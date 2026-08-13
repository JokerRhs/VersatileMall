from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

def register_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 生产环境改为指定域名
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )