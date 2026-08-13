from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 登录请求
class AdminLoginReq(BaseModel):
    username: str = Field(
        description="账号",
        min_length=3,
        max_length=32,
        json_schema_extra={"error_messages": {"max_length": "账号不能超过32个字符"}}
    )
    password: str = Field(
        description="明文密码",
        min_length=6,
        max_length=64,   # 小于72字节，彻底避开bcrypt限制
        json_schema_extra={"error_messages": {"max_length": "密码长度不能超过64个字符"}}
    )
# 登录返回
class AdminLoginResp(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin_id: int
    merchant_id: int
    username: str
    nickname: Optional[str]

# 管理员基础信息
class AdminInfo(BaseModel):
    id: int
    merchant_id: int
    username: str
    nickname: Optional[str]
    status: bool
    created_at: datetime

    class Config:
        from_attributes = True