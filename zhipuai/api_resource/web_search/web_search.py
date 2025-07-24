from __future__ import annotations

from typing import TYPE_CHECKING, List, Union, Dict, Optional
from ...types.sensitive_word_check import SensitiveWordCheckRequest
from ...core import NOT_GIVEN, Body, Headers, NotGiven, BaseAPI, maybe_transform, StreamResponse, deepcopy_minimal

import httpx

from ...core import (
    make_request_options,
)
import logging

from ...types.web_search import web_search_create_params
from ...types.web_search.web_search_resp import WebSearchResp

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..._client import ZhipuAI

__all__ = ["WebSearchApi"]


class WebSearchApi(BaseAPI):
    def __init__(self, client: "ZhipuAI") -> None:
        super().__init__(client)

    def web_search(
            self,
            *,
            request_id: Optional[str] | NotGiven = NOT_GIVEN,
            search_engine: Optional[str] | NotGiven = NOT_GIVEN,
            search_query: Optional[str] | NotGiven = NOT_GIVEN,
            user_id: Optional[str] | NotGiven = NOT_GIVEN,
            sensitive_word_check: Optional[SensitiveWordCheckRequest] | NotGiven = NOT_GIVEN,
            count: Optional[int] | NotGiven = NOT_GIVEN,
            search_domain_filter: Optional[str] | NotGiven = NOT_GIVEN,
            search_recency_filter: Optional[str] | NotGiven = NOT_GIVEN,
            content_size: Optional[str] | NotGiven = NOT_GIVEN,
            search_intent: Optional[bool] | NotGiven = NOT_GIVEN,
            location: Optional[str] | NotGiven = NOT_GIVEN,
            extra_headers: Headers | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebSearchResp:

        body = deepcopy_minimal(
            {
                "request_id": request_id,
                "search_engine": search_engine,
                "search_query": search_query,
                "user_id": user_id,
                "sensitive_word_check": sensitive_word_check,
                "count":count,
                "search_domain_filter": search_domain_filter,
                "search_recency_filter": search_recency_filter,
                "content_size": content_size,
                "search_intent": search_intent,
                "location": location
            })
        return self._post(
            "/web_search",
            body= maybe_transform(body, web_search_create_params.WebSearchCreatParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_body=extra_body, timeout=timeout
            ),
            cast_type=WebSearchResp
        )
