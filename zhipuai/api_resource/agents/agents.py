from __future__ import annotations

from typing import Union, List, Optional, TYPE_CHECKING, Dict

import httpx
import logging
from typing_extensions import Literal

from ...core import BaseAPI, deepcopy_minimal
from ...core import NotGiven, NOT_GIVEN, Headers, Query, Body
from ...core import make_request_options
from ...core import StreamResponse
from ...types.agents.agents_completion import AgentsCompletion
from ...types.agents.agents_completion_chunk import AgentsCompletionChunk
from ...types.sensitive_word_check import SensitiveWordCheckRequest

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..._client import ZhipuAI


class Agents(BaseAPI):

    def __init__(self, client: "ZhipuAI") -> None:
        super().__init__(client)

    def invoke(
            self,
            agent_id: Optional[str] | NotGiven = NOT_GIVEN,
            request_id: Optional[str] | NotGiven = NOT_GIVEN,
            stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
            messages: Union[str, List[str], List[int], object, None] | NotGiven = NOT_GIVEN,
            user_id: Optional[str] | NotGiven = NOT_GIVEN,
            custom_variables: object = NOT_GIVEN,
            sensitive_word_check: Optional[SensitiveWordCheckRequest] | NotGiven = NOT_GIVEN,
            extra_headers: Headers | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AgentsCompletion | StreamResponse[AgentsCompletionChunk]:
        body = deepcopy_minimal({
            "agent_id": agent_id,
            "request_id": request_id,
            "user_id": user_id,
            "messages": messages,
            "sensitive_word_check": sensitive_word_check,
            "stream": stream,
            "custom_variables": custom_variables
        })

        return self._post(
            "/v1/agents",
            body=body,
            options=make_request_options(
                extra_headers=extra_headers, extra_body=extra_body, timeout=timeout
            ),
            cast_type=AgentsCompletion,
            stream=stream or False,
            stream_cls=StreamResponse[AgentsCompletionChunk],
        )

    def async_result(
            self,
            agent_id: Optional[str] | NotGiven = NOT_GIVEN,
            async_id: Optional[str] | NotGiven = NOT_GIVEN,
            conversation_id: Optional[str] | NotGiven = NOT_GIVEN,
            custom_variables: object = NOT_GIVEN,
            extra_headers: Headers | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AgentsCompletion:
        body = deepcopy_minimal({
            "agent_id": agent_id,
            "async_id": async_id,
            "conversation_id": conversation_id,
            "custom_variables": custom_variables
        })
        return self._post(
            "/v1/agents/async-result",
            body=body,
            options=make_request_options(
                extra_headers=extra_headers, extra_body=extra_body, timeout=timeout
            ),
            cast_type=AgentsCompletion,
        )
