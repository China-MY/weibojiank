from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    """
    User model for authentication.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

class WeiboAccount(Base):
    """
    Weibo account to be monitored.
    """
    __tablename__ = "weibo_accounts"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(64), unique=True, index=True)
    screen_name = Column(String(255))
    last_update_time = Column(DateTime, nullable=True) # Last time the user posted a weibo
    last_check_time = Column(DateTime, default=datetime.utcnow) # Last time we checked
    status = Column(String(32), default="normal")
    check_interval = Column(Integer, default=3600)  # Check interval in seconds (default 1 hour)
    is_active = Column(Boolean, default=True)
    
    logs = relationship("CrawlLog", back_populates="account")

class CrawlLog(Base):
    """
    Log of crawling attempts.
    """
    __tablename__ = "crawl_logs"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("weibo_accounts.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String(32))
    message = Column(Text, nullable=True)
    
    account = relationship("WeiboAccount", back_populates="logs")

class SystemConfig(Base):
    """
    System configuration (key-value pairs).
    """
    __tablename__ = "system_configs"

    key = Column(String(64), primary_key=True, index=True)
    value = Column(Text, nullable=True)
    description = Column(String(255), nullable=True)
