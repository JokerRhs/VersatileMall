# VersatileMall
通用的开源企业级商城
技术栈：FastAPI + PostgreSQL + Redis + Pydantic V2 + SQLAlchemy 2.0 (异步) + Uvicorn/Gunicorn
业务目标前置：多商家 SaaS 商城后端（后续支撑：商家登录鉴权、不同商家数据隔离、前台商城 / 商家后台接口）
规范：分版本迭代、每版本附带完整文档、环境配置、启动方式、测试清单、风险注意事项。
版本规划总览（先约定迭代节奏）

版本	内容
V0.1	项目骨架、目录结构、环境变量、数据库连接、Redis 连接、全局异常、日志、健康检查、基础启动脚本（当前文档）
V0.2	数据库表结构（商家表、商家管理员表）、异步 ORM 模型、初始化 SQL 脚本
V0.3	统一响应封装、全局中间件、请求日志、跨域配置、路由模块化拆分
V0.4	JWT 鉴权工具、Redis 缓存工具、登录接口雏形、租户 (merchantId) 基础隔离工具类
V0.5	商家登录、token 签发、权限拦截、基础越权校验逻辑
V0.6	单元测试、接口自动化测试、Dockerfile、compose 本地一键部署
V0.7	生产部署参数、进程管理、日志切割、监控指标

	
V0.1 初始化前置操作（必须先执行）.
本地启动 PostgreSQL，新建数据库 "数据库名"
sql   CREATE DATABASE "数据库名";
启动 Redis（无密码 / 配置对应密码）.
.env 修改连接信息.

V0.1 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # linux/mac
venv\Scripts\activate     # windows
pip install -e ".[dev]"

V0.1 测试验证清单 
启动服务后访问：
首页：http://127.0.0.1:8000
文档地址：http://127.0.0.1:8000/api/v1/docs
健康检查：http://127.0.0.1:8000/api/v1/health
预期返回示例：
{
  "code": 200,
  "msg": "success",
  "data": {
    "postgres": true,
    "redis": true
  }
}

V0.2 测试验证清单
启动服务，访问健康接口，pg、redis 均为 true
访问接口文档 /api/v1/docs，无跨域报错
执行 alembic upgrade head，数据库自动创建两张表
主动制造异常，观察日志格式化输出

V0.2 重要注意事项文档
ORM 模型新增表必须在 app/models/init.py 导入，否则 alembic 自动检测不到表结构
alembic 异步模式不要使用同步引擎，必须使用上面提供的 env.py 模板
密码一律使用 bcrypt 哈希存储，禁止明文（V0.3 封装工具类）
所有业务表后续新增必须增加 merchant_id 字段，保证租户隔离
生产环境 CORS 不要设置 allow_origins=["*"]，配置前端域名列表
全局自定义异常统一抛出 BusinessException，不要直接抛 HTTPException，方便统一返回格式
server_default=func.now() 时间由数据库生成，不要在应用层赋值
