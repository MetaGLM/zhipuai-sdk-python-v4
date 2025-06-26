from __future__ import annotations

from typing import List, Optional

from typing_extensions import Literal, Required, TypedDict
__all__ = ["TranscriptionsParam"]

from ..sensitive_word_check import SensitiveWordCheckRequest

class TranscriptionsParam(TypedDict, total=False):
    model: str
    """模型编码"""
    temperature:float
    """采样温度"""
    stream: bool
    """是否流式输出"""
    sensitive_word_check: Optional[SensitiveWordCheckRequest]
    request_id: str
    """由用户端传参，需保证唯一性；用于区分每次请求的唯一标识，用户端不传时平台会默认生成。"""
    user_id: str
    """用户端。"""