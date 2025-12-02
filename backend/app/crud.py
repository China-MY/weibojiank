from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from passlib.context import CryptContext
from datetime import datetime
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt_sha256", "bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    try:
        if hashed_password.startswith("$2"):
            import bcrypt
            return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False

def get_password_hash(password):
    return pwd_context.hash(password)

# User Operations
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user_credentials(db: AsyncSession, user_id: int, username: Optional[str], password: Optional[str]):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    u = result.scalars().first()
    if not u:
        return None
    if username:
        u.username = username
    if password:
        u.hashed_password = get_password_hash(password)
    await db.commit()
    await db.refresh(u)
    return u

# Weibo Account Operations
async def get_weibo_accounts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.WeiboAccount).offset(skip).limit(limit))
    return result.scalars().all()

async def get_active_weibo_accounts(db: AsyncSession):
    result = await db.execute(select(models.WeiboAccount).filter(models.WeiboAccount.is_active == True))
    return result.scalars().all()

async def create_weibo_account(db: AsyncSession, account: schemas.WeiboAccountCreate):
    db_account = models.WeiboAccount(**account.dict())
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account

async def get_weibo_account_by_uid(db: AsyncSession, uid: str):
    result = await db.execute(select(models.WeiboAccount).filter(models.WeiboAccount.uid == uid))
    return result.scalars().first()

async def delete_weibo_account(db: AsyncSession, account_id: int):
    result = await db.execute(select(models.WeiboAccount).filter(models.WeiboAccount.id == account_id))
    account = result.scalars().first()
    if account:
        await db.delete(account)
        await db.commit()
        return True
    return False

async def update_weibo_account_status(db: AsyncSession, uid: str, last_update_time: datetime, status: str):
    result = await db.execute(select(models.WeiboAccount).filter(models.WeiboAccount.uid == uid))
    account = result.scalars().first()
    if account:
        account.last_update_time = last_update_time
        account.last_check_time = datetime.utcnow()
        account.status = status
        await db.commit()
        await db.refresh(account)
    return account
