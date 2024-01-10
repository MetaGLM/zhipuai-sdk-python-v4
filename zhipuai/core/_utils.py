from __future__ import annotations

from typing import Mapping

from ._base_type import NotGiven


def remove_notgiven_indict(obj):
    if obj is None or (not isinstance(obj, Mapping)):
        return obj
    return {key: value for key, value in obj.items() if not isinstance(value, NotGiven)}
