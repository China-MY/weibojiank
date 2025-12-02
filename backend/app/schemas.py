from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# WeiboAccount Schemas
class WeiboAccountBase(BaseModel):
    uid: str
    screen_name: str
    check_interval: Optional[int] = 3600

class WeiboAccountCreate(WeiboAccountBase):
    pass

class WeiboAccountUpdate(BaseModel):
    screen_name: Optional[str] = None
    check_interval: Optional[int] = None
    is_active: Optional[bool] = None

class WeiboAccount(WeiboAccountBase):
    id: int
    last_update_time: Optional[datetime] = None
    last_check_time: Optional[datetime] = None
    status: str
    is_active: bool

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# SystemConfig Schemas
class SystemConfigBase(BaseModel):
    key: str
    value: Optional[str] = None
    description: Optional[str] = None

class SystemConfigCreate(SystemConfigBase):
    pass

class SystemConfig(SystemConfigBase):
    class Config:
        from_attributes = True

class UserUpdateCredentials(BaseModel):
    current_password: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
