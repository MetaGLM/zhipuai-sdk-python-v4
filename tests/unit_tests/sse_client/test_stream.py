# -*- coding: utf-8 -*-
import unittest
from typing import Type, cast, Iterable
import pytest
import httpx
import inspect

import pydantic
from zhipuai import APIResponseValidationError
from zhipuai.core import BaseModel, StreamResponse, get_args, HttpClient, construct_type
from zhipuai.core._base_type import ResponseT
from zhipuai.types.chat.chat_completion_chunk import ChatCompletionChunk


class MockClient:

    _strict_response_validation: bool = False
    def _process_response_data(
            self,
            *,
            data: object,
            cast_type: Type[ResponseT],
            response: httpx.Response,
    ) -> ResponseT:
        pass


def test_stream_cls_chunk() -> None:
    MockClient._process_response_data = HttpClient._process_response_data

    def body() -> Iterable[bytes]:
        yield b'data: {"id":"8635243129834723621","created":1715329207,"model":"glm-4","choices":[{"index":0,"delta":{"role":"assistant","content":"1"}}]}\n\n'
        yield b'data: {"id":"8635243129834723621","created":1715329207,"model":"glm-4","choices":[{"index":0,"delta":{"role":"assistant","content":"2"}}]}\n\n'

    _stream_cls = StreamResponse[ChatCompletionChunk]
    http_response = httpx.Response(
        status_code=200,
        content=body()
    )

    stream_cls = _stream_cls(cast_type=cast(type, get_args(_stream_cls)[0]),
                             response=http_response,
                             client=MockClient()
                             )
    chat_completion_chunk1 = next(stream_cls)

    assert chat_completion_chunk1.choices[0].delta.content == "1"
    assert chat_completion_chunk1.choices[0].delta.role == "assistant"
    assert chat_completion_chunk1.choices[0].index == 0
    assert chat_completion_chunk1.model == "glm-4"
    chat_completion_chunk2 = next(stream_cls)
    assert chat_completion_chunk2.choices[0].delta.content == "2"
    assert chat_completion_chunk2.choices[0].delta.role == "assistant"
    assert chat_completion_chunk2.choices[0].index == 0
    assert chat_completion_chunk2.model == "glm-4"
