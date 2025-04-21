
from __future__ import annotations

from typing import Union, Optional, List
from typing_extensions import Literal, Required, TypedDict
from ...types.sensitive_word_check import SensitiveWordCheckRequest


__all__ = ["WebSearchCreatParams"]


class WebSearchCreatParams(TypedDict):

    search_engine: str
    """搜索引擎"""

    search_query: str
    """搜索query文本"""

    request_id: str
    """由用户端传参，需保证唯一性；用于区分每次请求的唯一标识，用户端不传时平台会默认生成。"""

    user_id: str
    """用户端。"""

    sensitive_word_check: Optional[SensitiveWordCheckRequest]
