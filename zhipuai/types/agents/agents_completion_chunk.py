from typing import List, Optional, Dict, Any

from ...core import BaseModel

__all__ = [
    "AgentsCompletionUsage",
    "AgentsCompletionChunk",
    "AgentsChoice",
    "AgentsChoiceDelta"
]


class AgentsChoiceDelta(BaseModel):
    content: Optional[object] = None
    role: Optional[str] = None


class AgentsChoice(BaseModel):
    delta: AgentsChoiceDelta
    finish_reason: Optional[str] = None
    index: int


class AgentsCompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class AgentsError(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None


class AgentsCompletionChunk(BaseModel):
    agent_id: Optional[str] = None
    conversation_id: Optional[str] = None
    id: Optional[str] = None
    choices: List[AgentsChoice]
    usage: Optional[AgentsCompletionUsage] = None
    error: Optional[AgentsError] = None