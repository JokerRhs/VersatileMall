from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.exceptions import BusinessException, business_exception_handler, global_exception_handler
from app.core.middleware import register_cors
from app.database.redis_client import init_redis, close_redis
from app.api.v1 import api_v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动事件
    await init_redis()
    print("✅ Redis 连接成功")
    yield
    # 关闭事件
    await close_redis()
    print("🛑 Redis 连接已关闭")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc"
)

# 注册中间件
register_cors(app)

# 注册路由
app.include_router(api_v1_router, prefix=settings.API_PREFIX)

# 注册异常处理器
app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
@app.get("/")
async def root():
    return {"message": "Merchant Shop API Service Running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.ENV == "dev"
    )