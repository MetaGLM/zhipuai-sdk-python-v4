from typing import List
from pydantic import BaseModel

class Voice(BaseModel):
    id: int
    voiceId: str
    voiceName: str
    voiceType: str
    voiceStatus: str
    voiceText: str
    createTime: str
    updateTime: str

class VoiceListResponse(BaseModel):
    code: int
    msg: str
    data: List[Voice]
    success: bool

class VoiceAddResponse(BaseModel):
    code: int
    msg: str
    data: Voice
    success: bool 