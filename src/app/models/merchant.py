from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, ForeignKey, Column
from app.models.base import Base
from app.schemas.enums import MerchantStatus

class Merchant(Base):
    __tablename__ = "merchant"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="商家ID")
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True, comment="商家唯一编码(URL路由使用)")
    name: Mapped[str] = mapped_column(String(128), comment="商家名称")
    # 改成字符串存储状态
    status = Column(String(20), default=MerchantStatus.NORMAL.value, nullable=False)

class MerchantAdmin(Base):
    __tablename__ = "merchant_admin"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    merchant_id: Mapped[int] = mapped_column(ForeignKey("merchant.id"), index=True, comment="关联商家ID")
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True, comment="登录账号")
    password_hash: Mapped[str] = mapped_column(String(256), comment="密码哈希，不存储明文")
    nickname: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="管理员昵称")
    # 改成字符串存储状态
    status = Column(String(20), default=MerchantStatus.NORMAL.value, nullable=False)
    # 缺少这一行就会报上面的错
    is_super = Column(Boolean, default=False, nullable=False)