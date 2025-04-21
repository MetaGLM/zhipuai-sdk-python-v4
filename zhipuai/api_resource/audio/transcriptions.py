from __future__ import annotations

from typing import TYPE_CHECKING, List, Mapping, cast, Optional, Dict
from ...types.audio import transcriptions_create_param

import httpx
import logging
from typing_extensions import Literal

from ...core import BaseAPI, deepcopy_minimal, maybe_transform, drop_prefix_image_data
from ...core import make_request_options
from ...core import StreamResponse
from ...types.chat.chat_completion import Completion
from ...types.chat.chat_completion_chunk import ChatCompletionChunk
from ...types.sensitive_word_check import SensitiveWordCheckRequest
from ...core import NOT_GIVEN, Body, Headers, NotGiven, FileTypes
from zhipuai.core._utils import extract_files


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..._client import ZhipuAI


__all__ = ["Transcriptions"]

class Transcriptions(BaseAPI):
    def __init__(self, client: "ZhipuAI") -> None:
        super().__init__(client)

    def create(
            self,
            *,
            file: FileTypes,
            model: str,
            request_id: Optional[str] | NotGiven = NOT_GIVEN,
            user_id: Optional[str] | NotGiven = NOT_GIVEN,
            stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
            temperature: Optional[float] | NotGiven = NOT_GIVEN,
            sensitive_word_check: Optional[SensitiveWordCheckRequest] | NotGiven = NOT_GIVEN,
            extra_headers: Headers | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN
    ) -> Completion | StreamResponse[ChatCompletionChunk]:
        if temperature is not None and temperature != NOT_GIVEN:
            if temperature <= 0:
                temperature = 0.01
            if temperature >= 1:
                temperature = 0.99

        body = deepcopy_minimal({
            "model": model,
            "file": file,
            "request_id": request_id,
            "user_id": user_id,
            "temperature": temperature,
            "sensitive_word_check": sensitive_word_check,
            "stream": stream
        })
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        if files:
            extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/audio/transcriptions",
            body=maybe_transform(body, transcriptions_create_param.TranscriptionsParam),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_body=extra_body, timeout=timeout
            ),
            cast_type=Completion,
            stream=stream or False,
            stream_cls=StreamResponse[ChatCompletionChunk],
        )
