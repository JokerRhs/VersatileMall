from typing import Optional

from fastapi import APIRouter, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.api.dependencies import DBDep
from app.schemas import AdminLoginReq, AdminLoginResp
from app.models.merchant import MerchantAdmin
from app.core.security import verify_password, create_access_token
from app.common.enums import ErrCode
from app.core.exceptions import BusinessException
from app.common.response import ApiResp
from app.api.dependencies import AuthDep, AdminContext
from app.database.redis_client import get_redis

router = APIRouter(prefix="/admin/auth", tags=["管理员-认证"])

@router.post("/login", response_model=ApiResp)
async def login(req: AdminLoginReq, db: AsyncSession = DBDep):
    # 查询账号
    stmt = select(MerchantAdmin).where(MerchantAdmin.username == req.username)
    admin = (await db.execute(stmt)).scalar_one_or_none()
    if not admin:
        raise BusinessException(ErrCode.USER_NOT_EXIST, "账号不存在")
    if not admin.status:
        raise BusinessException(ErrCode.ACCOUNT_DISABLED, "账号已禁用")
    if not verify_password(req.password, admin.password_hash):
        raise BusinessException(ErrCode.PASSWORD_ERROR, "密码错误")

    token = create_access_token(admin_id=admin.id, merchant_id=admin.merchant_id)
    data = AdminLoginResp(
        access_token=token,
        admin_id=admin.id,
        merchant_id=admin.merchant_id,
        username=admin.username,
        nickname=admin.nickname
    )
    return ApiResp.success(data=data)

@router.post("/logout", response_model=ApiResp)
async def logout(
    ctx: AdminContext = AuthDep,
    authorization: Optional[str] = Header(None)
):
    token = authorization.removeprefix("Bearer ")
    # 黑名单有效期同token有效期
    try:
        redis_cli = get_redis()
    except RuntimeError:
        raise BusinessException(ErrCode.FAIL, "缓存服务未初始化")
    
    await redis_cli.setex(f"token:revoke:{token}", timedelta(minutes=120), "1")
    return ApiResp.success(msg="登出成功")

@router.get("/profile", response_model=ApiResp)
async def profile(ctx: AdminContext = AuthDep):
    """获取当前登录管理员信息（租户ID自动携带）"""
    data = {
        "admin_id": ctx.admin_id,
        "merchant_id": ctx.merchant_id
    }
    return ApiResp.success(data=data)