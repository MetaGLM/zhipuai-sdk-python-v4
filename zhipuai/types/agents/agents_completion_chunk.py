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


class AgentsCompletionChunk(BaseModel):
    agent_id: Optional[str] = None
    id: Optional[str] = None
    choices: List[AgentsChoice]
    created: Optional[int] = None
    usage: Optional[AgentsCompletionUsage] = None