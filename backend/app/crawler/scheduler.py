from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.future import select
from app.database import SessionLocal
from app import models, crud
from app.crawler.weibo_spider import fetch_weibo_updates
import logging
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.future import select
import requests

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

async def crawl_job():
    """
    Periodic job to check all active weibo accounts.
    """
    logger.info("Starting crawl job...")
    async with SessionLocal() as db:
        # Get System Config (Cookie)
        cookie_config = await db.execute(select(models.SystemConfig).where(models.SystemConfig.key == "weibo_cookie"))
        cookie_val = cookie_config.scalar_one_or_none()
        cookie = cookie_val.value if cookie_val else None
        proxies_cfg = await db.execute(select(models.SystemConfig).where(models.SystemConfig.key == "proxies"))
        proxies_val = proxies_cfg.scalar_one_or_none()
        proxies = []
        if proxies_val and proxies_val.value:
            proxies = [p.strip() for p in proxies_val.value.splitlines() if p.strip()]
        webhook_cfg = await db.execute(select(models.SystemConfig).where(models.SystemConfig.key == "webhook_url"))
        webhook_val = webhook_cfg.scalar_one_or_none()
        webhook_url = webhook_val.value if webhook_val else None

        accounts = await crud.get_active_weibo_accounts(db)
        
        for account in accounts:
            logger.info(f"Checking account: {account.screen_name} (UID: {account.uid})")
            
            if account.last_check_time and (datetime.utcnow() - account.last_check_time).total_seconds() < (account.check_interval or 3600):
                continue
            last_update_time, message = fetch_weibo_updates(account.uid, cookie, proxies)

            
            status = "normal"
            if not last_update_time:
                status = "error"
                # If error, maybe keep old time or set to None? 
                # We'll just log it.
            else:
                # Check if expired (e.g. > N days)
                # This logic can be done here or in a separate check.
                # User asked: "When found > N days not updated, record to reminder list"
                # We update the DB state here.
                pass

            if last_update_time:
                account.last_update_time = last_update_time
                account.status = "normal"
            account.last_check_time = datetime.now(ZoneInfo('Asia/Shanghai')).replace(tzinfo=None)
            
            # Create Log
            log = models.CrawlLog(
                account_id=account.id,
                status="success" if last_update_time else "failure",
                message=message
            )
            db.add(log)
            await db.commit()
            
            days_threshold_cfg = await db.execute(select(models.SystemConfig).where(models.SystemConfig.key == "expired_days"))
            cfg_val = days_threshold_cfg.scalar_one_or_none()
            days_threshold = int(cfg_val.value) if cfg_val and cfg_val.value else 1
            if account.last_update_time:
                threshold_dt = datetime.now(ZoneInfo('Asia/Shanghai')).replace(tzinfo=None) - timedelta(days=days_threshold)
                if account.last_update_time < threshold_dt:
                    account.status = "expired"
                    await db.commit()
            if webhook_url:
                try:
                    now = datetime.now(ZoneInfo('Asia/Shanghai')).replace(tzinfo=None)
                    overdue_days = 0
                    if account.last_update_time:
                        overdue_days = (now - account.last_update_time).days
                    trigger_push = (not last_update_time) or (account.status == "expired")
                    if trigger_push:
                        content = f"{account.screen_name} 异常，已超过{max(overdue_days, days_threshold)}天未更新；最后更新时间：{account.last_update_time}"
                        requests.post(webhook_url, json={"msgtype":"text","text":{"content":content}}, timeout=10)
                except Exception:
                    pass
            
            # Respect the 5s interval rule
            await asyncio.sleep(5)
            
    logger.info("Crawl job finished.")

def start_scheduler():
    scheduler.add_job(crawl_job, 'interval', minutes=30)
    async def daily_webhook_job():
        async with SessionLocal() as db:
            cfg_time = await db.execute(select(models.SystemConfig).where(models.SystemConfig.key == "webhook_daily_time"))
            val_time = cfg_time.scalar_one_or_none()
            cfg_url = await db.execute(select(models.SystemConfig).where(models.SystemConfig.key == "webhook_url"))
            val_url = cfg_url.scalar_one_or_none()
            if not val_time or not val_time.value or not val_url or not val_url.value:
                return

            now = datetime.now(ZoneInfo('Asia/Shanghai')).replace(tzinfo=None)
            if val_time.value != now.strftime("%H:%M"):
                return

            try:
                accounts = await crud.get_weibo_accounts(db, limit=10000)
                days_cfg = await db.execute(select(models.SystemConfig).where(models.SystemConfig.key == "expired_days"))
                days_val = days_cfg.scalar_one_or_none()
                threshold_days = int(days_val.value) if days_val and days_val.value else 1
                lines = []
                for a in accounts:
                    if a.last_update_time and (now - a.last_update_time).days >= threshold_days:
                        lines.append(f"{a.screen_name}：已超过{(now - a.last_update_time).days}天未更新；最后更新时间：{a.last_update_time}")
                content = "每日提醒\n" + ("\n".join(lines) if lines else "暂无超期提醒")
                requests.post(val_url.value, json={"msgtype":"text","text":{"content":content}}, timeout=10)
            except Exception:
                pass
    scheduler.add_job(daily_webhook_job, 'cron', minute='*')
    scheduler.start()
