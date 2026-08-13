from pydantic import BaseModel, Field
from typing import Any, Optional
from app.common.enums import ErrCode

class ApiResp(BaseModel):
    code: int = Field(description="状态码")
    msg: str = Field(description="提示信息")
    data: Optional[Any] = Field(None, description="业务数据")

    @classmethod
    def success(cls, data: Any = None, msg: str = "ok") -> "ApiResp":
        return cls(code=ErrCode.SUCCESS, msg=msg, data=data)

    @classmethod
    def fail(cls, code: int = ErrCode.FAIL, msg: str = "fail") -> "ApiResp":
        return cls(code=code, msg=msg)