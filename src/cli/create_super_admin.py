import asyncio
import typer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.core.security import hash_password
from app.models.merchant import Merchant
from app.models.merchant import MerchantAdmin
from app.schemas.enums import MerchantStatus, AdminStatus

app = typer.Typer()


@app.command()
def create(
    merchant_code: str = typer.Option("M001", help="商家编码，唯一"),
    merchant_name: str = typer.Option("默认主商家", help="商家名称"),
    admin_username: str = typer.Option("superadmin", help="管理员账号"),
    admin_password: str = typer.Option("123456", help="管理员密码，<=72字节"),
    admin_nickname: str = typer.Option("超级管理员", help="管理员昵称"),
):
    """一键初始化商家+超级管理员"""
    asyncio.run(
        _async_create(
            merchant_code, merchant_name, admin_username, admin_password, admin_nickname
        )
    )


async def _async_create(
    merchant_code: str,
    merchant_name: str,
    admin_username: str,
    admin_password: str,
    admin_nickname: str,
):
    db: AsyncSession = await anext(get_db())
    try:
        # 1.判断商家是否存在 —— 使用ORM select，不要 __table__.select()
        result = await db.execute(
            select(Merchant).where(Merchant.code == merchant_code)
        )
        merchant = result.scalar_one_or_none()
        merchant_id: int

        if merchant:
            typer.echo(f"商家[{merchant_code}]已存在，id={merchant.id}")
            merchant_id = merchant.id
        else:
            new_merchant = Merchant(
                code=merchant_code,
                name=merchant_name,
                status=MerchantStatus.NORMAL.value,
            )
            db.add(new_merchant)
            await db.commit()
            await db.refresh(new_merchant)
            merchant_id = new_merchant.id
            typer.echo(f"✅ 创建商家成功 id={merchant_id} code={merchant_code}")

        # 2.判断管理员账号是否存在
        admin_result = await db.execute(
            select(MerchantAdmin).where(MerchantAdmin.username == admin_username)
        )
        admin = admin_result.scalar_one_or_none()

        if admin:
            typer.echo(f"⚠️ 管理员账号[{admin_username}]已存在，跳过创建")
            return

        # bcrypt限制：密码截断72字节
        raw_pwd = admin_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
        hashed_pwd = hash_password(raw_pwd)

        new_admin = MerchantAdmin(
            merchant_id=merchant_id,
            username=admin_username,
            password_hash=hashed_pwd,
            nickname=admin_nickname,
            status=AdminStatus.NORMAL.value,
            is_super=True,
        )
        db.add(new_admin)
        await db.commit()
        await db.refresh(new_admin)
        typer.echo(f"✅ 超级管理员创建完成！")
        typer.echo(f"   商家ID: {merchant_id}")
        typer.echo(f"   账号: {admin_username}")
        typer.echo(f"   密码: {admin_password}")

    except Exception as e:
        await db.rollback()
        typer.echo(f"❌ 执行失败: {str(e)}", err=True)
        raise
    finally:
        await db.close()

if __name__ == "__main__":
    app()
