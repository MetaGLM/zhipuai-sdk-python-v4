from __future__ import annotations

import contextlib
import gc
import os
import json
import asyncio
import inspect
import tracemalloc
from typing import Any, Union, cast, Dict
from unittest import mock

import httpx
import pytest
from respx import MockRouter
from typing_extensions import Iterator
from zhipuai.core import _errors, BaseModel

from zhipuai.core._http_client import ZHIPUAI_DEFAULT_TIMEOUT, make_request_options
from zhipuai import ZhipuAI, APIResponseValidationError, ZhipuAIError, APITimeoutError
from zhipuai._client import HttpClient
from zhipuai.core._request_opt import FinalRequestOptions
from zhipuai.core._sse_client import StreamResponse
from zhipuai.core._errors import (
    # ZhipuAIError,
    APIStatusError,
    # APITimeoutError,
    # APIResponseValidationError,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:2333")
api_key = "Key.secret"


def _get_params(client: HttpClient[Any, Any]) -> dict[str, str]:
    request = client._build_request(
        FinalRequestOptions.construct(method="get", url="/foo")
    )
    url = httpx.URL(request.url)
    return dict(url.params)


@contextlib.contextmanager
def update_env(**new_env: str) -> Iterator[None]:
    old = os.environ.copy()

    try:
        os.environ.update(new_env)

        yield None
    finally:
        os.environ.clear()
        os.environ.update(old)


class MockResponse(httpx.Response):
    def __init__(self, status_code: int, json_data: dict):
        super().__init__(status_code=status_code, json=json_data)


class TestZhipuAI:
    client = ZhipuAI(base_url=base_url, api_key=api_key)

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/foo").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        response = self.client.post("/foo", cast_type=object)
        assert response == {"foo": "bar"}

    def test_request_timeout(self) -> None:
        opts = FinalRequestOptions.construct(method="get", url="/foo")

        request = self.client._build_request(opts)
        timeout = httpx.Timeout(**request.extensions["timeout"])  # type: ignore
        assert timeout == ZHIPUAI_DEFAULT_TIMEOUT

        request = self.client._build_request(
            FinalRequestOptions.construct(method="get", url="/foo", timeout=httpx.Timeout(100.0))
        )
        timeout = httpx.Timeout(**request.extensions["timeout"])  # type: ignore
        assert timeout == httpx.Timeout(100.0)

    def test_client_timeout_option(self) -> None:
        client = ZhipuAI(base_url=base_url, api_key=api_key, timeout=httpx.Timeout(0))
        request = client._build_request(
            FinalRequestOptions.construct(method="get", url="/foo")
        )
        timeout = httpx.Timeout(**request.extensions["timeout"])  # type: ignore
        assert timeout == httpx.Timeout(0)

    def test_http_client_timeout_option(self) -> None:
        # custom timeout given to the httpx client should be used
        with httpx.Client(timeout=None) as http_client:
            client = ZhipuAI(
                base_url=base_url, api_key=api_key, http_client=http_client
            )

            request = client._build_request(
                FinalRequestOptions.construct(method="get", url="/foo")
            )
            timeout = httpx.Timeout(**request.extensions["timeout"])  # type: ignore
            assert timeout == httpx.Timeout(None)

        # no timeout given to the httpx client should not use the httpx default
        with httpx.Client() as http_client:
            client = ZhipuAI(
                base_url=base_url, api_key=api_key, http_client=http_client
            )

            request = client._build_request(
                FinalRequestOptions.construct(method="get", url="/foo")
            )
            timeout = httpx.Timeout(**request.extensions["timeout"])  # type: ignore
            assert timeout == ZHIPUAI_DEFAULT_TIMEOUT

        # explicitly passing the default timeout currently results in it being ignored
        with httpx.Client(timeout=httpx._config.DEFAULT_TIMEOUT_CONFIG) as http_client:
            client = ZhipuAI(
                base_url=base_url, api_key=api_key, http_client=http_client
            )

            request = client._build_request(
                FinalRequestOptions.construct(method="get", url="/foo")
            )
            timeout = httpx.Timeout(**request.extensions["timeout"])  # type: ignore
            assert timeout == ZHIPUAI_DEFAULT_TIMEOUT  # our default

    def test_default_headers_option(self) -> None:
        client = ZhipuAI(
            base_url=base_url, api_key=api_key, custom_headers={"X-Foo": "bar"}
        )
        request = client._build_request(
            FinalRequestOptions.construct(method="get", url="/foo")
        )
        assert request.headers.get("x-foo") == "bar"
        assert request.headers.get("x-request-sdk") == "zhipu-sdk-python"

        client2 = ZhipuAI(
            base_url=base_url,
            api_key=api_key,
            custom_headers={
                "X-Foo": "zhipu",
                "x-request-sdk": "custom-sdk-python",
            },
        )
        request = client2._build_request(
            FinalRequestOptions.construct(method="get", url="/foo")
        )
        assert request.headers.get("x-foo") == "zhipu"
        assert request.headers.get("x-request-sdk") == "custom-sdk-python"

    def test_validate_token_headers(self) -> None:
        client = ZhipuAI(base_url=base_url, api_key=api_key, disable_token_cache=False)
        request = client._build_request(
            FinalRequestOptions.construct(method="get", url="/foo")
        )
        from zhipuai.core._jwt_token import generate_token
        assert request.headers.get("Authorization") == f"Bearer {generate_token(api_key)}"

        with pytest.raises(ZhipuAIError):
            client2 = ZhipuAI(base_url=base_url, api_key=None)
            _ = client2

    def test_request_extra_headers(self) -> None:
        request = self.client._build_request(
            FinalRequestOptions.construct(
                method="post",
                url="/foo",
                **make_request_options(
                    extra_headers={"X-Foo": "Foo"}
                )
            )
        )

        assert request.headers.get("X-Foo") == "Foo"

    def test_base_url_setter(self) -> None:
        client = ZhipuAI(base_url="https://example.com/from_init", api_key=api_key, )
        assert client._base_url == "https://example.com/from_init/"

    def test_prepare_url(self):
        url = self.client._prepare_url("/path")
        assert url == "http://127.0.0.1:2333/path"

    def test_base_url_env(self) -> None:
        with update_env(ZHIPUAI_BASE_URL="http://localhost:5000/from/env"):
            client = ZhipuAI(api_key=api_key)
            assert client._base_url == "http://localhost:5000/from/env/"

    @pytest.mark.parametrize(
        "client",
        [
            ZhipuAI(base_url="http://localhost:5000/custom/path/", api_key=api_key, ),
            ZhipuAI(
                base_url="http://localhost:5000/custom/path/",
                api_key=api_key,
                http_client=httpx.Client(),
            ),
        ],
        ids=["standard", "custom http client"],
    )
    def test_base_url_trailing_slash(self, client: ZhipuAI) -> None:
        request = client._build_request(
            FinalRequestOptions.construct(
                method="post",
                url="/foo",
                json_data={"foo": "bar"},
            )
        )
        assert request.url == "http://localhost:5000/custom/path/foo"

    @pytest.mark.parametrize(
        "client",
        [
            ZhipuAI(base_url="http://localhost:5000/custom/path/", api_key=api_key, ),
            ZhipuAI(
                base_url="http://localhost:5000/custom/path/",
                api_key=api_key,
                http_client=httpx.Client(),
            ),
        ],
        ids=["standard", "custom http client"],
    )
    def test_absolute_request_url(self, client: ZhipuAI) -> None:
        request = client._build_request(
            FinalRequestOptions.construct(
                method="post",
                url="https://myapi.com/foo",
                json_data={"foo": "bar"},
            )
        )
        assert request.url == "https://myapi.com/foo"

    def test_make_status_error(self):
        response = MockResponse(status_code=400, json_data={"error": "Bad Request"})
        with pytest.raises(_errors.APIRequestFailedError) as exc:
            raise self.client._make_status_error(response) from None
        assert exc.value.args[0] == 'Error code: 400, with error text {"error": "Bad Request"}'

        response = MockResponse(status_code=401, json_data={"error": "Unauthorized"})
        with pytest.raises(_errors.APIAuthenticationError) as exc:
            raise self.client._make_status_error(response) from None
        assert exc.value.args[0] == 'Error code: 401, with error text {"error": "Unauthorized"}'

        response = MockResponse(status_code=429, json_data={"error": "Rate Limit Exceeded"})
        with pytest.raises(_errors.APIReachLimitError) as exc:
            raise self.client._make_status_error(response) from None
        assert exc.value.args[0] == 'Error code: 429, with error text {"error": "Rate Limit Exceeded"}'

        response = MockResponse(status_code=500, json_data={"error": "Internal Server Error"})
        with pytest.raises(_errors.APIInternalError) as exc:
            raise self.client._make_status_error(response) from None
        assert exc.value.args[0] == 'Error code: 500, with error text {"error": "Internal Server Error"}'

        response = MockResponse(status_code=503, json_data={"error": "Service Unavailable"})
        with pytest.raises(_errors.APIServerFlowExceedError) as exc:
            raise self.client._make_status_error(response) from None
        assert exc.value.args[0] == 'Error code: 503, with error text {"error": "Service Unavailable"}'

        response = MockResponse(status_code=400, json_data={"error": "Unknown Error"})
        with pytest.raises(_errors.APIRequestFailedError) as exc:
            raise self.client._make_status_error(response) from None
        assert exc.value.args[0] == 'Error code: 400, with error text {"error": "Unknown Error"}'

    @pytest.mark.respx(base_url=base_url)
    def test_default_stream_cls(self, respx_mock: MockRouter) -> None:
        class Model(BaseModel):
            name: str

        respx_mock.post("/foo").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        response = self.client.post("/foo",
                                    cast_type=Model,
                                    stream=True,
                                    stream_cls=StreamResponse[Model])
        assert isinstance(response, StreamResponse)

    @pytest.mark.respx(base_url=base_url)
    def test_retrying_timeout_errors_doesnt_leak(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/chat/completions").mock(side_effect=httpx.TimeoutException("Test timeout error"))

        with pytest.raises(APITimeoutError):
            self.client.post(
                "/chat/completions",
                body=dict(
                    messages=[
                        {
                            "role": "user",
                            "content": "Say this is a test",
                        }
                    ],
                    model="gpt-3.5-turbo",
                ),
                cast_type=httpx.Response,
                options={"headers": {"X-Stainless-Streamed-Raw-Response": "true"}},
            )

        assert len(self.client._client._transport._pool._requests) == 0

    @pytest.mark.respx(base_url=base_url)
    def test_get(self, respx_mock: MockRouter) -> None:
        respx_mock.get("/foo").mock(
            return_value=httpx.Response(
                200,
                content=json.dumps({"result": "success"}),
                headers={"content-type": "application/json"},
            )
        )

        response = self.client.get("/foo", cast_type=Dict[str, object])
        assert response == {"result": "success"}

        respx_mock.get("/boo").mock(
            return_value=httpx.Response(
                200,
                content=json.dumps({"result": "success"}),
                headers={"content-type": "application/text"},
            )
        )

        response = self.client.get("/boo", cast_type=Dict[str, object])
        assert response == '{"result": "success"}'

    @pytest.mark.respx(base_url=base_url)
    def test_post(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/foo").mock(
            return_value=httpx.Response(
                200,
                content=json.dumps({"result": "success"}),
                headers={"content-type": "application/json"},
            )
        )

        response = self.client.post("/foo", cast_type=Dict[str, object], body={"foo": "bar"})
        assert response == {"result": "success"}

    @pytest.mark.respx(base_url=base_url)
    def test_patch(self, respx_mock: MockRouter) -> None:
        respx_mock.patch("/foo").mock(
            return_value=httpx.Response(
                200,
                content=json.dumps({"result": "success"}),
                headers={"content-type": "application/json"},
            )
        )

        response = self.client.patch("/foo", cast_type=Dict[str, object], body={"foo": "bar"})
        assert response == {"result": "success"}

    @pytest.mark.respx(base_url=base_url)
    def test_delete(self, respx_mock: MockRouter) -> None:
        respx_mock.delete("/foo").mock(
            return_value=httpx.Response(
                200,
                content=json.dumps({"result": "success"}),
                headers={"content-type": "application/json"},
            )
        )

        response = self.client.delete("/foo", cast_type=Dict[str, object], body={"foo": "bar"})
        assert response == {"result": "success"}

    def test_is_closed(self):
        assert self.client.is_closed() is False

    def test_close(self):
        self.client.close()
        assert self.client.is_closed() is True
