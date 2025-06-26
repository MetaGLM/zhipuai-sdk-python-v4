from typing import List, Optional

from ...core import BaseModel

__all__ = [
    "SearchIntentResp",
    "SearchResultResp",
]


class SearchIntentResp(BaseModel):
    query: str
    # 搜索优化 query
    intent: str
    # 判断的意图类型
    keywords: str
    # 搜索关键词


class SearchResultResp(BaseModel):
    title: str
    # 标题
    link: str
    # 链接
    content: str
    # 内容
    icon: str
    # 图标
    media: str
    # 来源媒体
    refer: str
    # 角标序号 [ref_1]
    publish_date:  str
    # 发布时间

class WebSearchResp(BaseModel):
    created: Optional[int] = None
    request_id: Optional[str] = None
    id: Optional[str] = None
    search_intent: Optional[SearchIntentResp]
    search_result: Optional[SearchResultResp]

