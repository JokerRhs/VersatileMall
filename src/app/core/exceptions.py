from fastapi import Request
from fastapi.responses import JSONResponse
from app.common.response import ApiResp
from app.common.enums import ErrCode
from app.core.logger import app_log

# 自定义业务异常
class BusinessException(Exception):
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

# 全局异常处理器
async def business_exception_handler(request: Request, exc: BusinessException):
    resp = ApiResp.fail(code=exc.code, msg=exc.msg)
    return JSONResponse(content=resp.model_dump())

async def global_exception_handler(request: Request, exc: Exception):
    app_log.error("系统异常", exc_info=exc)
    resp = ApiResp.fail(code=ErrCode.FAIL, msg="服务器内部异常")
    return JSONResponse(content=resp.model_dump())

# 常用异常快捷构造
# class ErrCode:
#     AUTH_FAILED = 401
#     FORBIDDEN = 403
#     NOT_FOUND = 404
#     PARAM_ERROR = 400
#     MERCHANT_DISABLE = 410