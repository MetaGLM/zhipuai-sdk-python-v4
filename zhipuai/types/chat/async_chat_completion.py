from typing import List, Optional

from pydantic import BaseModel

from .chat_completion import CompletionChoice, CompletionUsage

__all__ = ["AsyncTaskStatus"]


class AsyncTaskStatus(BaseModel):
    id: str
    request_id: str
    model: Optional[str] = None
    task_status: str


class AsyncCompletion(BaseModel):
    id: str
    request_id: Optional[str] = None
    model: str
    task_status: str
    choices: List[CompletionChoice]
    usage: CompletionUsage