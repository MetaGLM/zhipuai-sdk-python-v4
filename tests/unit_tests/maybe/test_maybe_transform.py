# -*- coding: utf-8 -*-
import unittest
from typing import Type, cast, Iterable, TypedDict
import pytest
import httpx
import inspect

from zhipuai.core import maybe_transform
from zhipuai.types import batch_create_params


def test_response_joblist_model_cast() -> None:
    params = maybe_transform(
        {
            "completion_window": "/v1/chat/completions",
            "endpoint": None,
            "metadata": {
                "key": "value"
            },
        },
        batch_create_params.BatchCreateParams,
    )
    assert isinstance(params, dict)
