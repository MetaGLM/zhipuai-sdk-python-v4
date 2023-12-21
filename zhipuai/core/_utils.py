from __future__ import annotations

import functools
from typing import Mapping

from ._base_type import NotGiven
from ._sse_client import StreamResponse


def remove_notgiven_indict(obj):
    if obj is None or (not isinstance(obj, Mapping)):
        return obj
    return {key: value for key, value in obj.items() if not isinstance(value, NotGiven)}
