from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas, database
from app.routers.auth import get_current_user
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.future import select
from app.models import SystemConfig
from app.crawler.weibo_spider import fetch_weibo_updates, fetch_weibo_updates_pc
import json
from pathlib import Path
import requests
from sqlalchemy import update

router = APIRouter(
    prefix="/weibo",
    tags=["weibo"],
    responses={404: {"detail": "Not found"}},
)

@router.get("/list", response_model=List[schemas.WeiboAccount])
async def read_weibo_accounts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    accounts = await crud.get_weibo_accounts(db, skip=skip, limit=limit)
    return accounts

@router.get("/expired", response_model=List[schemas.WeiboAccount])
async def read_expired_accounts(days: int = 3, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """
    Get accounts that haven't updated for 'days' days.
    """
    accounts = await crud.get_weibo_accounts(db, limit=1000)
    expired_accounts = []
    now = datetime.now(ZoneInfo('Asia/Shanghai')).replace(tzinfo=None)
    for account in accounts:
        ref = account.last_check_time or now
        threshold_dt = ref - timedelta(days=days)
        if account.last_update_time and account.last_update_time < threshold_dt:
            expired_accounts.append(account)
            
    return expired_accounts

@router.get("/expired_report")
async def read_expired_report(days: int = 0, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    cfg = await db.execute(select(SystemConfig).where(SystemConfig.key == "expired_days"))
    cfg_val = cfg.scalar_one_or_none()
    threshold_days = days if days > 0 else int(cfg_val.value) if cfg_val and cfg_val.value else 3
    accounts = await crud.get_weibo_accounts(db, limit=1000)
    now = datetime.now(ZoneInfo('Asia/Shanghai')).replace(tzinfo=None)
    report = []
    for a in accounts:
        ref = a.last_check_time or now
        threshold_dt = ref - timedelta(days=threshold_days)
        if a.last_update_time and a.last_update_time < threshold_dt:
            overdue_days = (ref - a.last_update_time).days
            report.append({
                "screen_name": a.screen_name,
                "overdue_days": overdue_days
            })
    return report

@router.post("/check/{uid}")
async def check_account(uid: str, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    cookie_cfg = await db.execute(select(SystemConfig).where(SystemConfig.key == "weibo_cookie"))
    cookie_val = cookie_cfg.scalar_one_or_none()
    cookie = cookie_val.value if cookie_val else None
    proxies_cfg = await db.execute(select(SystemConfig).where(SystemConfig.key == "proxies"))
    proxies_val = proxies_cfg.scalar_one_or_none()
    proxies = []
    if proxies_val and proxies_val.value:
        proxies = [p.strip() for p in proxies_val.value.splitlines() if p.strip()]
    last_update_time, message = fetch_weibo_updates(uid, cookie, proxies)
    account = await crud.get_weibo_account_by_uid(db, uid)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if last_update_time:
        account.last_update_time = last_update_time
        account.status = "normal"
    account.last_check_time = datetime.now(ZoneInfo('Asia/Shanghai')).replace(tzinfo=None)
    await db.commit()
    await db.refresh(account)
    return {"last_update_time": account.last_update_time, "message": message}

@router.get("/parse_file")
async def parse_file(uid: str, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    cfg = await db.execute(select(SystemConfig).where(SystemConfig.key == "weibo_cookie"))
    cfg_val = cfg.scalar_one_or_none()
    cookie = cfg_val.value if cfg_val else None
    try:
        latest_created_at, message = fetch_weibo_updates_pc(uid, cookie)
        return {"created_at": latest_created_at, "message": message}
    except Exception as e:
        return {"created_at": None, "message": str(e)}

@router.post("/batch_interval")
async def batch_set_interval(seconds: int | None = Query(None), payload: dict | None = Body(None), db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    seconds = seconds if seconds is not None else (payload.get("seconds") if payload else None)
    if seconds is None:
        raise HTTPException(status_code=400, detail="缺少 seconds 参数")
    try:
        seconds = int(seconds)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="seconds 参数必须为整数")

    if seconds < 3600 or seconds > 21600:
        raise HTTPException(status_code=400, detail="检查间隔需在1-6小时之间")
    
    stmt = update(models.WeiboAccount).values(check_interval=seconds)
    await db.execute(stmt)
    await db.commit()
    return {"ok": True, "seconds": seconds}

@router.post("/add", response_model=schemas.WeiboAccount)
async def add_weibo_account(account: schemas.WeiboAccountCreate, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_account = await crud.get_weibo_account_by_uid(db, uid=account.uid)
    if db_account:
        raise HTTPException(status_code=400, detail="Account already exists")
    return await crud.create_weibo_account(db=db, account=account)

@router.delete("/remove/{account_id}")
async def remove_weibo_account(account_id: int, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    success = await crud.delete_weibo_account(db, account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"ok": True}
@router.post("/webhook_test")
async def webhook_test(db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    cfg = await db.execute(select(SystemConfig).where(SystemConfig.key == "webhook_url"))
    val = cfg.scalar_one_or_none()
    if not val or not val.value:
        raise HTTPException(status_code=400, detail="未配置Webhook")
    now = datetime.now(ZoneInfo('Asia/Shanghai')).replace(tzinfo=None)
    try:
        payload = {"msgtype": "text", "text": {"content": f"Webhook测试成功，当前时间：{now}"}}
        requests.post(val.value, json=payload, timeout=10)
        return {"ok": True}
    except Exception:
        raise HTTPException(status_code=500, detail="推送失败")
@router.post("/push_summary")
async def push_summary(days: int | None = Query(None), db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    cfg_url = await db.execute(select(SystemConfig).where(SystemConfig.key == "webhook_url"))
    val_url = cfg_url.scalar_one_or_none()
    if not val_url or not val_url.value:
        raise HTTPException(status_code=400, detail="未配置Webhook")
    days_cfg = await db.execute(select(SystemConfig).where(SystemConfig.key == "expired_days"))
    days_val = days_cfg.scalar_one_or_none()
    threshold_days = days if days is not None else (int(days_val.value) if days_val and days_val.value else 1)
    accounts = await crud.get_weibo_accounts(db, limit=10000)
    now = datetime.now(ZoneInfo('Asia/Shanghai')).replace(tzinfo=None)
    abn = []
    nor = []
    for a in accounts:
        ref = a.last_check_time or now
        od = (ref - a.last_update_time).days if a.last_update_time else threshold_days
        if (not a.last_update_time) or od >= threshold_days:
            abn.append(f"{a.screen_name}：已超过{od}天未更新；最后更新时间：{a.last_update_time}")
        else:
            nor.append(f"{a.screen_name}：最后更新时间：{a.last_update_time}")
    lines = ["监测结果汇总", f"异常（{len(abn)}）:", *(abn if abn else ["无"]), f"正常（{len(nor)}）:", *(nor if nor else ["无"])]
    content = "\n".join(lines)
    try:
        requests.post(val_url.value, json={"msgtype":"text","text":{"content":content}}, timeout=10)
        return {"ok": True}
    except Exception:
        raise HTTPException(status_code=500, detail="推送失败")
