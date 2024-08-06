from __future__ import annotations

from typing import Union, List, Optional, TYPE_CHECKING, Dict

import httpx
import logging
from typing_extensions import Literal

from ...core import BaseAPI, deepcopy_minimal, maybe_transform, drop_prefix_image_data
from ...core import NotGiven, NOT_GIVEN, Headers, Query, Body
from ...core import make_request_options
from ...core import StreamResponse
from ...types.chat.chat_completion import Completion
from ...types.chat.chat_completion_chunk import ChatCompletionChunk
from ...types.chat.code_geex import code_geex_params

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..._client import ZhipuAI


class Completions(BaseAPI):
    def __init__(self, client: "ZhipuAI") -> None:
        super().__init__(client)

    def create(
            self,
            *,
            model: str,
            request_id: Optional[str] | NotGiven = NOT_GIVEN,
            user_id: Optional[str] | NotGiven = NOT_GIVEN,
            do_sample: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
            stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
            temperature: Optional[float] | NotGiven = NOT_GIVEN,
            top_p: Optional[float] | NotGiven = NOT_GIVEN,
            max_tokens: int | NotGiven = NOT_GIVEN,
            seed: int | NotGiven = NOT_GIVEN,
            messages: Union[str, List[str], List[int], object, None],
            stop: Optional[Union[str, List[str], None]] | NotGiven = NOT_GIVEN,
            sensitive_word_check: Optional[object] | NotGiven = NOT_GIVEN,
            tools: Optional[object] | NotGiven = NOT_GIVEN,
            tool_choice: str | NotGiven = NOT_GIVEN,
            meta: Optional[Dict[str,str]] | NotGiven = NOT_GIVEN,
            extra: Optional[code_geex_params.CodeGeexExtra] | NotGiven = NOT_GIVEN,
            extra_headers: Headers | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Completion | StreamResponse[ChatCompletionChunk]:
        logger.debug(f"temperature:{temperature}, top_p:{top_p}")
        if temperature is not None and temperature != NOT_GIVEN:

            if temperature <= 0:
                do_sample = False
                temperature = 0.01
                # logger.warning("temperature:取值范围是：(0.0, 1.0) 开区间，do_sample重写为:false（参数top_p temperture不生效）")
            if temperature >= 1:
                temperature = 0.99
                # logger.warning("temperature:取值范围是：(0.0, 1.0) 开区间")
        if top_p is not None and top_p != NOT_GIVEN:

            if top_p >= 1:
                top_p = 0.99
                # logger.warning("top_p:取值范围是：(0.0, 1.0) 开区间，不能等于 0 或 1")
            if top_p <= 0:
                top_p = 0.01
                # logger.warning("top_p:取值范围是：(0.0, 1.0) 开区间，不能等于 0 或 1")

        logger.debug(f"temperature:{temperature}, top_p:{top_p}")
        if isinstance(messages, List):
            for item in messages:
                if item.get('content'):
                    item['content'] = drop_prefix_image_data(item['content'])

        body = deepcopy_minimal({
            "model": model,
            "request_id": request_id,
            "user_id": user_id,
            "temperature": temperature,
            "top_p": top_p,
            "do_sample": do_sample,
            "max_tokens": max_tokens,
            "seed": seed,
            "messages": messages,
            "stop": stop,
            "sensitive_word_check": sensitive_word_check,
            "stream": stream,
            "tools": tools,
            "tool_choice": tool_choice,
            "meta": meta,
            "extra": maybe_transform(extra, code_geex_params.CodeGeexExtra),
        })
        return self._post(
            "/chat/completions",
            body=body,
            options=make_request_options(
                extra_headers=extra_headers, extra_body=extra_body, timeout=timeout
            ),
            cast_type=Completion,
            stream=stream or False,
            stream_cls=StreamResponse[ChatCompletionChunk],
        )


