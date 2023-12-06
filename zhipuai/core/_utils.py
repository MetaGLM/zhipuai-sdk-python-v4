from __future__ import annotations

import functools
from typing import Mapping

from zhipuai.core._base_type import NotGiven
from zhipuai.core._sse_client import StreamResponse


def remove_notgiven_indict(obj):
    if obj is None or (not isinstance(obj, Mapping)):
        return obj
    return {key: value for key, value in obj.items() if not isinstance(value, NotGiven)}


def to_json_response_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        kwargs['cast_type'] = object
        kwargs['stream_cls'] = StreamResponse[object]

        result = func(*args, **kwargs)
        return result

    return wrapper
