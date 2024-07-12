from __future__ import annotations

from typing import List, Optional

from typing_extensions import Literal, Required, TypedDict

__all__ = ["VideoCreateParams"]


class VideoCreateParams(TypedDict, total=False):
    model: str
    """模型编码"""
    prompt: str
    """所需视频的文本描述"""
    request_id: str
    """由用户端传参，需保证唯一性；用于区分每次请求的唯一标识，用户端不传时平台会默认生成。"""
