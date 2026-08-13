import sys
import logging
from loguru import logger
from app.core.config import settings

# 移除默认handler
logger.remove()

log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

# 控制台输出
logger.add(
    sys.stderr,
    format=log_format,
    level=settings.LOG_LEVEL,
    enqueue=True
)

# 对外暴露
app_log = logger