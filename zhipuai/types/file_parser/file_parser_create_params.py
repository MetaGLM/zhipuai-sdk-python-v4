from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict
from ...core import NOT_GIVEN, Body, Headers, NotGiven, FileTypes


__all__ = ["FileParserCreateParams", "FileParserDownloadParams"]


class FileParserCreateParams(TypedDict):
    file: FileTypes
    """上传的文件"""
    file_type: str
    """文件类型"""
    tool_type: Literal["simple", "doc2x", "tencent", "zhipu-pro"]
    """工具类型"""


class FileParserDownloadParams(TypedDict):
    task_id: str
    """解析任务id"""
    format_type: Literal["text", "download_link"]
    """结果返回类型"""

