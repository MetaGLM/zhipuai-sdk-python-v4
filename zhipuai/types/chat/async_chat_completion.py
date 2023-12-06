from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel

__all__ = ["AsyncCompletion"]


class AsyncCompletion(BaseModel):
    id: str
    request_id: str
    model: str
    task_status: str
