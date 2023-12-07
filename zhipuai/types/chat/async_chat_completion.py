from typing import List, Optional
from typing_extensions import Literal
from .chat_completion import CompletionChoice,CompletionUsage
from pydantic import BaseModel

__all__ = ["AsyncTaskStatus"]


class AsyncTaskStatus(BaseModel):
    id: str
    request_id: str
    model: Optional[str] = None
    task_status: str


class AsyncCompletion(BaseModel):
    id: str
    request_id: str
    model: str
    task_status: str
    choices: List[CompletionChoice]
    usage: CompletionUsage