from __future__ import annotations

from typing import List, Optional

from typing_extensions import Literal, Required, TypedDict

__all__ = ["VideoCreateParams"]


class VideoCreateParams(TypedDict, total=False):
    model: str
    """模型编码"""
    prompt: str
    """所需视频的文本描述"""
    image_url: str
    """支持 URL 或者 Base64、传入 image 奖进行图生视频
     * 图片格式：
     *   图片大小："""
    prompt_opt_model: str
    """调用指定模型进行对 prompt 优化，推荐使用 GLM-4-Air 和 GLM-4-Flash。如未指定，则直接使用原始 prompt。"""
    request_id: str
    """由用户端传参，需保证唯一性；用于区分每次请求的唯一标识，用户端不传时平台会默认生成。"""
