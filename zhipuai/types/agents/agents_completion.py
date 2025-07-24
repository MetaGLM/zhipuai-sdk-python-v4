from typing import List, Optional

from ...core import BaseModel

__all__ = ["AgentsCompletion", "AgentsCompletionUsage"]

class AgentsCompletionMessage(BaseModel):
    content: Optional[object] = None
    role: str

class AgentsCompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class AgentsCompletionChoice(BaseModel):
    index: int
    finish_reason: str
    message: AgentsCompletionMessage

class AgentsError(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None


class AgentsCompletion(BaseModel):
    agent_id: Optional[str] = None
    conversation_id: Optional[str] = None
    status: Optional[str] = None
    choices: List[AgentsCompletionChoice]
    request_id: Optional[str] = None
    id: Optional[str] = None
    usage: Optional[AgentsCompletionUsage] = None
    error: Optional[AgentsError] = None

