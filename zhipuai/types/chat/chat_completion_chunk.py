from typing import List, Optional, Dict, Any

from ...core import BaseModel

__all__ = [
    "CompletionUsage",
    "ChatCompletionChunk",
    "Choice",
    "ChoiceDelta",
    "ChoiceDeltaFunctionCall",
    "ChoiceDeltaToolCall",
    "ChoiceDeltaToolCallFunction",
    "AudioCompletionChunk"
]


class ChoiceDeltaFunctionCall(BaseModel):
    arguments: Optional[str] = None
    name: Optional[str] = None


class ChoiceDeltaToolCallFunction(BaseModel):
    arguments: Optional[str] = None
    name: Optional[str] = None


class ChoiceDeltaToolCall(BaseModel):
    index: int
    id: Optional[str] = None
    function: Optional[ChoiceDeltaToolCallFunction] = None
    type: Optional[str] = None

class AudioCompletionChunk(BaseModel):
    id: Optional[str] = None
    data: Optional[str] = None
    expires_at: Optional[int] = None


class ChoiceDelta(BaseModel):
    content: Optional[str] = None
    role: Optional[str] = None
    reasoning_content: Optional[str] = None
    tool_calls: Optional[List[ChoiceDeltaToolCall]] = None
    audio: Optional[AudioCompletionChunk] = None


class Choice(BaseModel):
    delta: ChoiceDelta
    finish_reason: Optional[str] = None
    index: int

class PromptTokensDetails(BaseModel):
    cached_tokens: int

class CompletionTokensDetails(BaseModel):
    reasoning_tokens: int

class CompletionUsage(BaseModel):
    prompt_tokens: int
    prompt_tokens_details: Optional[PromptTokensDetails] = None
    completion_tokens: int
    completion_tokens_details: Optional[CompletionTokensDetails] = None
    total_tokens: int

class ChatCompletionChunk(BaseModel):
    id: Optional[str] = None
    choices: List[Choice]
    created: Optional[int] = None
    model: Optional[str] = None
    usage: Optional[CompletionUsage] = None
    extra_json: Dict[str, Any]
