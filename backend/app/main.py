from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, weibo, settings
from app.crawler import scheduler
import asyncio
from app import crud, database, schemas
from sqlalchemy.future import select
from app.models import SystemConfig

app = FastAPI(title="Weibo Update Monitor")


# CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(weibo.router)
app.include_router(settings.router)

@app.on_event("startup")
async def startup_event():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed default admin user if not exists
    async with database.SessionLocal() as db:
        admin = await crud.get_user_by_username(db, "boyueadmin")
        if not admin:
            await crud.create_user(db, schemas.UserCreate(username="boyueadmin", password="boyue2025@123"))
        # Seed default configs
        cfg_days = await db.execute(select(SystemConfig).where(SystemConfig.key == "expired_days"))
        if not cfg_days.scalar_one_or_none():
            db.add(SystemConfig(key="expired_days", value="1", description="提醒阈值(天)"))
            await db.commit()
    
    # Start scheduler
    scheduler.start_scheduler()

@app.get("/")
def read_root():
    return {"message": "Welcome to Weibo Update Monitor API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=18880, reload=True)
