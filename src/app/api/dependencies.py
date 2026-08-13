from fastapi import Depends, Header, Request
from typing import Optional
from app.database.session import get_db
from app.core.security import parse_token
from app.common.enums import ErrCode
from app.core.exceptions import BusinessException
from app.database.redis_client import get_redis

# DB会话依赖
DBDep = Depends(get_db)

# 当前登录管理员上下文
class AdminContext:
    def __init__(self, admin_id: int, merchant_id: int):
        self.admin_id = admin_id
        self.merchant_id = merchant_id

async def get_current_admin(
    # request: Request,
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> AdminContext:
    # print("请求方法：", request.method)
    # print("请求头:", dict(request.headers))
    # print("authorization原始值：", repr(authorization))
    if not authorization or not authorization.startswith("Bearer "):
        raise BusinessException(ErrCode.AUTH_FAILED, "缺少授权令牌")
    token = authorization.removeprefix("Bearer ")

    # 校验黑名单（登出失效）
    try:
        redis_cli = get_redis()
    except RuntimeError:
        raise BusinessException(ErrCode.FAIL, "缓存服务未初始化")
    
    if await redis_cli.exists(f"token:revoke:{token}"):
        raise BusinessException(ErrCode.TOKEN_REVOKED, "token已失效，请重新登录")

    payload = parse_token(token)
    admin_id = int(payload["sub"])
    merchant_id = int(payload["merchant_id"])
    return AdminContext(admin_id=admin_id, merchant_id=merchant_id)

# 鉴权依赖快捷注入
AuthDep = Depends(get_current_admin)