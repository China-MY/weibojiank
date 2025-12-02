from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import schemas, database, models
from app.routers.auth import get_current_user
from typing import List

router = APIRouter(
    prefix="/settings",
    tags=["settings"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[schemas.SystemConfig])
async def read_settings(db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.SystemConfig))
    return result.scalars().all()

@router.post("/", response_model=schemas.SystemConfig)
async def create_or_update_setting(config: schemas.SystemConfigCreate, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.SystemConfig).where(models.SystemConfig.key == config.key))
    db_config = result.scalar_one_or_none()
    if db_config:
        db_config.value = config.value
        db_config.description = config.description
        await db.commit()
        await db.refresh(db_config)
        return db_config
    new_config = models.SystemConfig(key=config.key, value=config.value, description=config.description)
    db.add(new_config)
    await db.commit()
    await db.refresh(new_config)
    return new_config

@router.get("/{key}", response_model=schemas.SystemConfig)
async def read_setting(key: str, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.SystemConfig).where(models.SystemConfig.key == key))
    db_config = result.scalar_one_or_none()
    if db_config is None:
        raise HTTPException(status_code=404, detail="Config not found")
    return db_config
