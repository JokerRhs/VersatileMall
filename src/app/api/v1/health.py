from fastapi import APIRouter
from app.common.response import ApiResp
from app.database.session import engine
from app.database.redis_client import get_redis
import logging

router = APIRouter(tags=["健康检查"])
logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check():
    # 检测数据库
    try:
        async with engine.connect():
            pg_ok = True
    except Exception as e:
        logger.error("Postgres连接失败", exc_info=e)
        pg_ok = False

    # 检测redis
    try:
        r = get_redis()
        await r.ping()
        redis_ok = True
    except Exception as e:
        logger.error("Redis连接失败", exc_info=e)
        redis_ok = False

    return ApiResp.success(data={
        "postgres": pg_ok,
        "redis": redis_ok
    })