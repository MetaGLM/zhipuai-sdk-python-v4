from __future__ import annotations

from typing import Union, List, Optional, TYPE_CHECKING

import httpx
from typing_extensions import Literal

from ...core import BaseAPI
from ...core import NotGiven, NOT_GIVEN, Headers, Body
from ...core import make_request_options
from ...types.chat.async_chat_completion import AsyncTaskStatus, AsyncCompletion

if TYPE_CHECKING:
    from ..._client import ZhipuAI


class AsyncCompletions(BaseAPI):
    def __init__(self, client: "ZhipuAI") -> None:
        super().__init__(client)


    def create(
            self,
            *,
            model: str,
            request_id: Optional[str] | NotGiven = NOT_GIVEN,
            do_sample: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
            temperature: Optional[float] | NotGiven = NOT_GIVEN,
            top_p: Optional[float] | NotGiven = NOT_GIVEN,
            max_tokens: int | NotGiven = NOT_GIVEN,
            seed: int | NotGiven = NOT_GIVEN,
            messages: Union[str, List[str], List[int], List[List[int]], None],
            stop: Optional[Union[str, List[str], None]] | NotGiven = NOT_GIVEN,
            sensitive_word_check: Optional[object] | NotGiven = NOT_GIVEN,
            tools: Optional[object] | NotGiven = NOT_GIVEN,
            tool_choice: str | NotGiven = NOT_GIVEN,
            meta: Optional[Dict[str,str]] | NotGiven = NOT_GIVEN,
            extra_headers: Headers | None = None,
            extra_body: Body | None = None,
            disable_strict_validation: Optional[bool] | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncTaskStatus:
        _cast_type = AsyncTaskStatus

        if disable_strict_validation:
            _cast_type = object
        return self._post(
            "/async/chat/completions",
            body={
                "model": model,
                "request_id": request_id,
                "temperature": temperature,
                "top_p": top_p,
                "do_sample": do_sample,
                "max_tokens": max_tokens,
                "seed": seed,
                "messages": messages,
                "stop": stop,
                "sensitive_word_check": sensitive_word_check,
                "tools": tools,
                "tool_choice": tool_choice,
                "meta": meta,
            },
            options=make_request_options(
                extra_headers=extra_headers, extra_body=extra_body, timeout=timeout
            ),
            cast_type=_cast_type,
            stream=False,
        )

    def retrieve_completion_result(
        self,
        id: str,
        extra_headers: Headers | None = None,
        extra_body: Body | None = None,
        disable_strict_validation: Optional[bool] | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Union[AsyncCompletion, AsyncTaskStatus]:
        _cast_type = Union[AsyncCompletion,AsyncTaskStatus]
        if disable_strict_validation:
            _cast_type = object
        return self._get(
            path=f"/async-result/{id}",
            cast_type=_cast_type,
            options=make_request_options(
                extra_headers=extra_headers, extra_body=extra_body, timeout=timeout
            ),
        )


