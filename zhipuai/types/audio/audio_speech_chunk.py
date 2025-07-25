from typing import List, Optional, Dict, Any

from ...core import BaseModel

__all__ = [
    "AudioSpeechChunk",
    "AudioError",
    "AudioSpeechChoice",
    "AudioSpeechDelta"
]


class AudioSpeechDelta(BaseModel):
    content: Optional[str] = None
    role: Optional[str] = None


class AudioSpeechChoice(BaseModel):
    delta: AudioSpeechDelta
    finish_reason: Optional[str] = None
    index: int

class AudioError(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None


class AudioSpeechChunk(BaseModel):
    choices: List[AudioSpeechChoice]
    request_id: Optional[str] = None
    created: Optional[int] = None
    error: Optional[AudioError] = None