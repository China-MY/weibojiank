from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from urllib.parse import quote_plus
from pathlib import Path


def _load_env_from_file():
    root = Path(__file__).resolve().parents[1]
    env_file = root / ".env"
    if env_file.exists():
        try:
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if not line or line.strip().startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip()
        except Exception:
            pass


_load_env_from_file()

DB_DRIVER = "mysql"
user = os.getenv("DB_USER", "root")
password = os.getenv("DB_PASSWORD", "boyue1!Z")
host = os.getenv("DB_HOST", "222.184.49.22")
port = os.getenv("DB_PORT", "3307")
name = os.getenv("DB_NAME", "weibopyjiank")
encoded_pw = quote_plus(password)
SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{user}:{encoded_pw}@{host}:{port}/{name}?charset=utf8mb4&connect_timeout=10"
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=1800,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
