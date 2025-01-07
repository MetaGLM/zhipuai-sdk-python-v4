from __future__ import annotations

from typing import List, Optional

from typing_extensions import Literal, Required, TypedDict
__all__ = ["AudioCustomizationParam"]

from ..sensitive_word_check import SensitiveWordCheckRequest

class AudioCustomizationParam(TypedDict, total=False):
    model: str
    """模型编码"""
    input: str
    """需要生成语音的文本"""
    voice_text: str
    """需要生成语音的音色"""
    response_format: str
    """需要生成语音文件的格式"""
    sensitive_word_check: Optional[SensitiveWordCheckRequest]
    request_id: str
    """由用户端传参，需保证唯一性；用于区分每次请求的唯一标识，用户端不传时平台会默认生成。"""
    user_id: str
    """用户端。"""


