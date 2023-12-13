from typing import List, Optional

from pydantic import BaseModel

__all__ = ["Completion","CompletionUsage"]


class Function(BaseModel):
    arguments: str
    name: str


class CompletionMessageToolCall(BaseModel):
    id: str
    function: Function
    type: str


class CompletionMessage(BaseModel):
    content: Optional[str] = None
    role: str
    tool_calls: Optional[List[CompletionMessageToolCall]] = None


class CompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionChoice(BaseModel):
    index: int
    finish_reason: str
    message: CompletionMessage


class Completion(BaseModel):
    model: str
    created: int
    choices: List[CompletionChoice]
    request_id: str
    id: str
    usage: CompletionUsage


