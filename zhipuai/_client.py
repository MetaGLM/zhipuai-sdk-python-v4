from __future__ import annotations

from typing import Union, Mapping

from typing_extensions import override

from .core import _jwt_token
from .core._errors import ZhipuAIError
from .core._http_client import HttpClient, ZHIPUAI_DEFAULT_MAX_RETRIES
from .core._base_type import NotGiven, NOT_GIVEN
from zhipuai import api_resource
import os
import httpx
from httpx import Timeout


class ZhipuAI(HttpClient):
    chat: api_resource.chat
    api_key: str

    def __init__(
            self,
            *,
            api_key: str | None = None,
            base_url: str | httpx.URL | None = None,
            timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
            max_retries: int = ZHIPUAI_DEFAULT_MAX_RETRIES,
            http_client: httpx.Client | None = None,
            custom_headers: Mapping[str, str] | None = None
    ) -> None:
        if api_key is None:
            api_key = os.environ.get("ZHIPUAI_API_KEY")
        if api_key is None:
            raise ZhipuAIError("未提供api_key，请通过参数或环境变量提供")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("ZHIPUAI_BASE_URL")
        if base_url is None:
            base_url = f"https://open.bigmodel.cn/stage-api/paas/v4/"

        super().__init__(
            version="0.0.1",
            base_url=base_url,
            # max_retries=max_retries,
            timeout=timeout,
            custom_httpx_client=http_client,
            custom_headers=custom_headers,
        )
        self.chat = api_resource.chat.Chat(self)

    @property
    @override
    def _auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"{_jwt_token.generate_token(api_key)}"}

    def __del__(self) -> None:
        if not hasattr(self, "_has_custom_http_client") or not hasattr(self, "close"):
            # this can happen if the '__init__' method raised an error
            return

        if self._has_custom_http_client:
            return

        self.close()
