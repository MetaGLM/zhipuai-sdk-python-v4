from __future__ import annotations

from typing import Union, Mapping

from typing_extensions import override

from .core import _jwt_token
from .core import ZhipuAIError
from .core import HttpClient, ZHIPUAI_DEFAULT_MAX_RETRIES
from .core import NotGiven, NOT_GIVEN
from . import api_resource
import os
import httpx
from httpx import Timeout


class ZhipuAI(HttpClient):
    chat: api_resource.chat.Chat
    api_key: str
    _disable_token_cache: bool = True
    source_channel: str

    def __init__(
            self,
            *,
            api_key: str | None = None,
            base_url: str | httpx.URL | None = None,
            timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
            max_retries: int = ZHIPUAI_DEFAULT_MAX_RETRIES,
            http_client: httpx.Client | None = None,
            custom_headers: Mapping[str, str] | None = None,
            disable_token_cache: bool = True,
            _strict_response_validation: bool = False,
            source_channel: str | None = None
    ) -> None:
        if api_key is None:
            api_key = os.environ.get("ZHIPUAI_API_KEY")
        if api_key is None:
            raise ZhipuAIError("未提供api_key，请通过参数或环境变量提供")
        self.api_key = api_key
        self.source_channel = source_channel
        self._disable_token_cache = disable_token_cache

        if base_url is None:
            base_url = os.environ.get("ZHIPUAI_BASE_URL")
        if base_url is None:
            base_url = f"https://open.bigmodel.cn/api/paas/v4"
        from .__version__ import __version__
        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            custom_httpx_client=http_client,
            custom_headers=custom_headers,
            _strict_response_validation=_strict_response_validation,
        )
        self.chat = api_resource.chat.Chat(self)
        self.images = api_resource.images.Images(self)
        self.embeddings = api_resource.embeddings.Embeddings(self)
        self.files = api_resource.files.Files(self)
        self.fine_tuning = api_resource.fine_tuning.FineTuning(self)
        self.batches = api_resource.Batches(self)
        self.knowledge = api_resource.Knowledge(self)
        self.tools = api_resource.Tools(self)
        self.videos = api_resource.Videos(self)
        self.assistant = api_resource.Assistant(self)
        self.web_search = api_resource.WebSearchApi(self)
        self.audio = api_resource.audio.Audio(self)
        self.moderations = api_resource.moderation.Moderations(self)
        self.agents = api_resource.agents.Agents(self)

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        source_channel = self.source_channel or "python-sdk"
        if self._disable_token_cache:
            return {"Authorization": f"Bearer {api_key}","x-source-channel": source_channel}
        else:
            return {"Authorization": f"Bearer {_jwt_token.generate_token(api_key)}","x-source-channel": source_channel}

    def __del__(self) -> None:
        if (not hasattr(self, "_has_custom_http_client")
                or not hasattr(self, "close")
                or not hasattr(self, "_client")):
            # if the '__init__' method raised an error, self would not have client attr
            return

        if self._has_custom_http_client:
            return

        self.close()
