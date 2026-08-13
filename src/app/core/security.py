from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import jwt, JWTError
from app.core.config import settings
from app.common.enums import ErrCode
from app.core.exceptions import BusinessException

# ========== 密码工具（原生bcrypt，自主截断） ==========
def hash_password(plain_password: str) -> str:
    raw_bytes = plain_password.encode("utf-8")[:72]  # 强制截断72字节
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(raw_bytes, salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    raw_bytes = plain_password.encode("utf-8")[:72]
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(raw_bytes, hashed_bytes)

# ========== JWT工具 ==========
def create_access_token(
    admin_id: int,
    merchant_id: int,
    expire_minutes: Optional[int] = None
) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=expire_minutes or settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(admin_id),
        "merchant_id": merchant_id,
        "exp": expire
    }
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return token

def parse_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise BusinessException(ErrCode.TOKEN_INVALID, "token无效或已过期")