from typing import TypeVar , Generic,Optional,Any
from pydantic import BaseModel


T=TypeVar("T")

class BaseResp(BaseModel,Generic[T]):
    success:bool
    message:str
    data:Optional[T]=None
    error:Optional[Any]=None
    

class SuccessResp(BaseResp[T]):
    success:bool=True
    error:None=None


class ErrorResp(BaseResp[T]):
    success:bool=False

    