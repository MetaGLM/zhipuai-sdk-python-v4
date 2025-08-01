from __future__ import annotations

from typing import TYPE_CHECKING, List, Mapping, cast, Optional, Dict
from .transcriptions import Transcriptions

from zhipuai.core._utils import extract_files

from zhipuai.types.sensitive_word_check import SensitiveWordCheckRequest
from zhipuai.types.audio import AudioSpeechParams
from ...types.audio import audio_customization_param

from zhipuai.core import BaseAPI, maybe_transform, StreamResponse
from zhipuai.core import NOT_GIVEN, Body, Headers, NotGiven, FileTypes
from zhipuai.core import _legacy_response

import httpx
from ...core import BaseAPI, cached_property

from zhipuai.core import (
    make_request_options,
)
from zhipuai.core import deepcopy_minimal
from ...types.audio.audio_speech_chunk import AudioSpeechChunk

if TYPE_CHECKING:
    from zhipuai._client import ZhipuAI

__all__ = ["Audio"]


class Audio(BaseAPI):

    @cached_property
    def transcriptions(self) -> Transcriptions:
        return Transcriptions(self._client)

    def __init__(self, client: "ZhipuAI") -> None:
        super().__init__(client)

    def speech(
            self,
            *,
            model: str,
            input: str = None,
            voice: str = None,
            response_format: str = None,
            sensitive_word_check: Optional[SensitiveWordCheckRequest] | NotGiven = NOT_GIVEN,
            request_id: str = None,
            user_id: str = None,
            stream: bool = False,
            extra_headers: Headers | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
            encode_format: str,
    ) -> _legacy_response.HttpxBinaryResponseContent | StreamResponse[AudioSpeechChunk]:
        body = deepcopy_minimal(
            {
                "model": model,
                "input": input,
                "voice": voice,
                "stream": stream,
                "response_format": response_format,
                "sensitive_word_check": sensitive_word_check,
                "request_id": request_id,
                "user_id": user_id,
                "encode_format": encode_format
            }
        )
        return self._post(
            "/audio/speech",
            body=body,
            options=make_request_options(
                extra_headers=extra_headers, extra_body=extra_body, timeout=timeout
            ),
            cast_type=_legacy_response.HttpxBinaryResponseContent,
            stream= stream or False,
            stream_cls=StreamResponse[AudioSpeechChunk]
        )

    def customization(
            self,
            *,
            model: str,
            input: str = None,
            voice_text: str = None,
            voice_data: FileTypes = None,
            response_format: str = None,
            sensitive_word_check: Optional[SensitiveWordCheckRequest] | NotGiven = NOT_GIVEN,
            request_id: str = None,
            user_id: str = None,
            extra_headers: Headers | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> _legacy_response.HttpxBinaryResponseContent:
        body = deepcopy_minimal(
            {
                "model": model,
                "input": input,
                "voice_text": voice_text,
                "voice_data": voice_data,
                "response_format": response_format,
                "sensitive_word_check": sensitive_word_check,
                "request_id": request_id,
                "user_id": user_id
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["voice_data"]])

        if files:
            extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/audio/customization",
            body=maybe_transform(body, audio_customization_param.AudioCustomizationParam),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_body=extra_body, timeout=timeout
            ),
            cast_type=_legacy_response.HttpxBinaryResponseContent
        )