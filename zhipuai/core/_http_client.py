# -*- coding:utf-8 -*-
from __future__ import annotations

import inspect
from typing import (
    Any,
    Type,
    Union,
    cast,
    Mapping,
    TypeVar,
    Dict,
    overload
)

from random import random
import time
import httpx
import pydantic
from httpx import URL, Timeout

from . import _errors
from ._base_type import (
    NotGiven,
    ResponseT,
    Body,
    Headers,
    NOT_GIVEN,
    RequestFiles,
    Query,
    Data,
    Omit,
    AnyMapping,
    ModelBuilderProtocol,
    HttpxSendArgs,
)
from ._errors import APIResponseValidationError, APIStatusError, APITimeoutError, APIConnectionError
from ._files import make_httpx_files
from ._request_opt import FinalRequestOptions, UserRequestInput
from ._response import HttpResponse
from ._sse_client import StreamResponse
from ._utils import flatten, is_mapping, is_given
from ._base_models import construct_type
import logging
_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)

log: logging.Logger = logging.getLogger(__name__)


headers = {
    "Accept": "application/json",
    "Content-Type": "application/json; charset=UTF-8",
}


from httpx._config import DEFAULT_TIMEOUT_CONFIG as HTTPX_DEFAULT_TIMEOUT
RAW_RESPONSE_HEADER = "X-Stainless-Raw-Response"
ZHIPUAI_DEFAULT_TIMEOUT = httpx.Timeout(timeout=300.0, connect=8.0)
ZHIPUAI_DEFAULT_MAX_RETRIES = 3
ZHIPUAI_DEFAULT_LIMITS = httpx.Limits(max_connections=50, max_keepalive_connections=10)

INITIAL_RETRY_DELAY = 0.5
MAX_RETRY_DELAY = 8.0

class HttpClient:
    _client: httpx.Client
    _version: str
    _base_url: URL
    max_retries: int
    timeout: Union[float, Timeout, None]
    _limits: httpx.Limits
    _has_custom_http_client: bool
    _default_stream_cls: type[StreamResponse[Any]] | None = None

    def __init__(
            self,
            *,
            version: str,
            base_url: URL,
            max_retries: int = ZHIPUAI_DEFAULT_MAX_RETRIES,
            timeout: Union[float, Timeout, None],
            limits: Limits | None = None,
            custom_httpx_client: httpx.Client | None = None,
            custom_headers: Mapping[str, str] | None = None,
    ) -> None:
        if limits is not None:
            warnings.warn(
                "The `connection_pool_limits` argument is deprecated. The `http_client` argument should be passed instead",
                category=DeprecationWarning,
                stacklevel=3,
            )
            if http_client is not None:
                raise ValueError("The `http_client` argument is mutually exclusive with `connection_pool_limits`")
        else:
            limits = ZHIPUAI_DEFAULT_LIMITS

        if not is_given(timeout):
            if custom_httpx_client and custom_httpx_client.timeout != HTTPX_DEFAULT_TIMEOUT:
                timeout = custom_httpx_client.timeout
            else:
                timeout = ZHIPUAI_DEFAULT_TIMEOUT
        self.max_retries = max_retries
        self.timeout = timeout
        self._limits = limits
        self._has_custom_http_client = bool(custom_httpx_client)
        self._client = custom_httpx_client or httpx.Client(
            base_url=base_url,
            timeout=self.timeout,
            limits=limits,
        )
        self._version = version
        url = URL(url=base_url)
        if not url.raw_path.endswith(b"/"):
            url = url.copy_with(raw_path=url.raw_path + b"/")
        self._base_url = url
        self._custom_headers = custom_headers or {}

    def _prepare_url(self, url: str) -> URL:

        sub_url = URL(url)
        if sub_url.is_relative_url:
            request_raw_url = self._base_url.raw_path + sub_url.raw_path.lstrip(b"/")
            return self._base_url.copy_with(raw_path=request_raw_url)

        return sub_url

    @property
    def _default_headers(self):
        return \
            {
                "Accept": "application/json",
                "Content-Type": "application/json; charset=UTF-8",
                "ZhipuAI-SDK-Ver": self._version,
                "source_type": "zhipu-sdk-python",
                "x-request-sdk": "zhipu-sdk-python",
                **self.auth_headers,
                **self._custom_headers,
            }
    @property
    def custom_auth(self) -> httpx.Auth | None:
        return None

    @property
    def auth_headers(self):
        return {}

    def _prepare_headers(self, options: FinalRequestOptions) -> httpx.Headers:
        custom_headers = options.headers or {}
        headers_dict = _merge_mappings(self._default_headers, custom_headers)

        httpx_headers = httpx.Headers(headers_dict)

        return httpx_headers

    def _remaining_retries(
            self,
            remaining_retries: Optional[int],
            options: FinalRequestOptions,
    ) -> int:
        return remaining_retries if remaining_retries is not None else options.get_max_retries(self.max_retries)

    def _calculate_retry_timeout(
            self,
            remaining_retries: int,
            options: FinalRequestOptions,
            response_headers: Optional[httpx.Headers] = None,
    ) -> float:
        max_retries = options.get_max_retries(self.max_retries)

        # If the API asks us to wait a certain amount of time (and it's a reasonable amount), just do what it says.
        # retry_after = self._parse_retry_after_header(response_headers)
        # if retry_after is not None and 0 < retry_after <= 60:
        #     return retry_after

        nb_retries = max_retries - remaining_retries

        # Apply exponential backoff, but not more than the max.
        sleep_seconds = min(INITIAL_RETRY_DELAY * pow(2.0, nb_retries), MAX_RETRY_DELAY)

        # Apply some jitter, plus-or-minus half a second.
        jitter = 1 - 0.25 * random()
        timeout = sleep_seconds * jitter
        return timeout if timeout >= 0 else 0

    def _build_request(
            self,
            options: FinalRequestOptions
    ) -> httpx.Request:
        kwargs: dict[str, Any] = {}
        headers = self._prepare_headers(options)
        url = self._prepare_url(options.url)
        json_data = options.json_data
        if options.extra_json is not None:
            if json_data is None:
                json_data = cast(Body, options.extra_json)
            elif is_mapping(json_data):
                json_data = _merge_mappings(json_data, options.extra_json)
            else:
                raise RuntimeError(f"Unexpected JSON data type, {type(json_data)}, cannot merge with `extra_body`")

        content_type = headers.get("Content-Type")
        # multipart/form-data; boundary=---abc--
        if headers.get("Content-Type") == "multipart/form-data":
            if "boundary" not in content_type:
                # only remove the header if the boundary hasn't been explicitly set
                # as the caller doesn't want httpx to come up with their own boundary
                headers.pop("Content-Type")

            if json_data:
                kwargs["data"] = self._make_multipartform(json_data)

        return self._client.build_request(
            headers=headers,
            timeout=self.timeout if isinstance(options.timeout, NotGiven) else options.timeout,
            method=options.method,
            url=url,
            json=json_data,
            files=options.files,
            params=options.params,
            **kwargs,
        )

    def _object_to_formfata(self, key: str, value: Data | Mapping[object, object]) -> list[tuple[str, str]]:
        items = []

        if isinstance(value, Mapping):
            for k, v in value.items():
                items.extend(self._object_to_formfata(f"{key}[{k}]", v))
            return items
        if isinstance(value, (list, tuple)):
            for v in value:
                items.extend(self._object_to_formfata(key + "[]", v))
            return items

        def _primitive_value_to_str(val) -> str:
            # copied from httpx
            if val is True:
                return "true"
            elif val is False:
                return "false"
            elif val is None:
                return ""
            return str(val)

        str_data = _primitive_value_to_str(value)

        if not str_data:
            return []
        return [(key, str_data)]

    def _make_multipartform(self, data: Mapping[object, object]) -> dict[str, object]:

        items = flatten([self._object_to_formfata(k, v) for k, v in data.items()])

        serialized: dict[str, object] = {}
        for key, value in items:
            if key in serialized:
                raise ValueError(f"存在重复的键: {key};")
            serialized[key] = value
        return serialized

    def _parse_response(
            self,
            *,
            cast_type: Type[ResponseT],
            response: httpx.Response,
            stream: bool,
            options: FinalRequestOptions,
            stream_cls: type[StreamResponse[Any]] | None = None,
    ) -> HttpResponse:

        http_response = HttpResponse(
            raw_response=response,
            cast_type=cast_type,
            client=self,
            stream=stream,
            stream_cls=stream_cls
        )
        return http_response.parse()

    def _process_response_data(
            self,
            *,
            data: object,
            cast_type: type[ResponseT],
            response: httpx.Response,
    ) -> ResponseT:

        if data is None:
            return cast(ResponseT, None)

        if cast_type is object:
            return cast(ResponseT, data)

        try:
            if inspect.isclass(cast_type) and issubclass(cast_type, ModelBuilderProtocol):
                return cast(ResponseT, cast_type.build(response=response, data=data))

            return cast(ResponseT, construct_type(type_=cast_type, value=data))
        except pydantic.ValidationError as err:
            raise APIResponseValidationError(response=response, json_data=data) from err

    def _should_stream_response_body(self, request: httpx.Request) -> bool:
        return request.headers.get(RAW_RESPONSE_HEADER) == "stream"  # type: ignore[no-any-return]

    def _should_retry(self, response: httpx.Response) -> bool:
        # Note: this is not a standard header
        should_retry_header = response.headers.get("x-should-retry")

        # If the server explicitly says whether or not to retry, obey.
        if should_retry_header == "true":
            log.debug("Retrying as header `x-should-retry` is set to `true`")
            return True
        if should_retry_header == "false":
            log.debug("Not retrying as header `x-should-retry` is set to `false`")
            return False

        # Retry on request timeouts.
        if response.status_code == 408:
            log.debug("Retrying due to status code %i", response.status_code)
            return True

        # Retry on lock timeouts.
        if response.status_code == 409:
            log.debug("Retrying due to status code %i", response.status_code)
            return True

        # Retry on rate limits.
        if response.status_code == 429:
            log.debug("Retrying due to status code %i", response.status_code)
            return True

        # Retry internal errors.
        if response.status_code >= 500:
            log.debug("Retrying due to status code %i", response.status_code)
            return True

        log.debug("Not retrying")
        return False

    def is_closed(self) -> bool:
        return self._client.is_closed

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def request(
            self,
            cast_type: Type[ResponseT],
            options: FinalRequestOptions,
            remaining_retries: Optional[int] = None,
            *,
            stream: bool = False,
            stream_cls: type[StreamResponse] | None = None,
    ) -> ResponseT | StreamResponse:
        return self._request(
            cast_type=cast_type,
            options=options,
            stream=stream,
            stream_cls=stream_cls,
            remaining_retries=remaining_retries,
        )

    def _request(
            self,
            *,
            cast_type: Type[ResponseT],
            options: FinalRequestOptions,
            remaining_retries: int | None,
            stream: bool,
            stream_cls: type[StreamResponse] | None,
    ) -> ResponseT | StreamResponse:

        retries = self._remaining_retries(remaining_retries, options)
        request = self._build_request(options)

        kwargs: HttpxSendArgs = {}
        if self.custom_auth is not None:
            kwargs["auth"] = self.custom_auth
        try:
            response = self._client.send(
                request,
                stream=stream or self._should_stream_response_body(request=request),
                **kwargs,
            )
        except httpx.TimeoutException as err:
            log.debug("Encountered httpx.TimeoutException", exc_info=True)

            if retries > 0:
                return self._retry_request(
                    options,
                    cast_type,
                    retries,
                    stream=stream,
                    stream_cls=stream_cls,
                    response_headers=None,
                )

            log.debug("Raising timeout error")
            raise APITimeoutError(request=request) from err
        except Exception as err:
            log.debug("Encountered Exception", exc_info=True)

            if retries > 0:
                return self._retry_request(
                    options,
                    cast_type,
                    retries,
                    stream=stream,
                    stream_cls=stream_cls,
                    response_headers=None,
                )

            log.debug("Raising connection error")
            raise APIConnectionError(request=request) from err

        log.debug(
            'HTTP Request: %s %s "%i %s"', request.method, request.url, response.status_code, response.reason_phrase
        )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as err:  # thrown on 4xx and 5xx status code
            log.debug("Encountered httpx.HTTPStatusError", exc_info=True)

            if retries > 0 and self._should_retry(err.response):
                err.response.close()
                return self._retry_request(
                    options,
                    cast_type,
                    retries,
                    err.response.headers,
                    stream=stream,
                    stream_cls=stream_cls,
                )

            # If the response is streamed then we need to explicitly read the response
            # to completion before attempting to access the response text.
            if not err.response.is_closed:
                err.response.read()

            log.debug("Re-raising status error")
            raise self._make_status_error(err.response) from None


        return self._parse_response(
            cast_type=cast_type,
            options=options,
            response=response,
            stream=stream,
            stream_cls=stream_cls,
        )

    def _retry_request(
            self,
            options: FinalRequestOptions,
            cast_type: Type[ResponseT],
            remaining_retries: int,
            response_headers: httpx.Headers | None,
            *,
            stream: bool,
            stream_cls: type[StreamResponse] | None,
    ) -> ResponseT | StreamResponse:
        remaining = remaining_retries - 1
        if remaining == 1:
            log.debug("1 retry left")
        else:
            log.debug("%i retries left", remaining)

        timeout = self._calculate_retry_timeout(remaining, options, response_headers)
        log.info("Retrying request to %s in %f seconds", options.url, timeout)

        # In a synchronous context we are blocking the entire thread. Up to the library user to run the client in a
        # different thread if necessary.
        time.sleep(timeout)

        return self._request(
            options=options,
            cast_type=cast_type,
            remaining_retries=remaining,
            stream=stream,
            stream_cls=stream_cls,
        )

    @overload
    def get(
            self,
            path: str,
            *,
            cast_type: Type[ResponseT],
            options: UserRequestInput = {},
            stream: Literal[False] = False,
    ) -> ResponseT:
        ...

    @overload
    def get(
            self,
            path: str,
            *,
            cast_type: Type[ResponseT],
            options: UserRequestInput = {},
            stream: Literal[True],
            stream_cls: type[StreamResponse],
    ) -> StreamResponse:
        ...

    @overload
    def get(
            self,
            path: str,
            *,
            cast_type: Type[ResponseT],
            options: UserRequestInput = {},
            stream: bool,
            stream_cls: type[StreamResponse] | None = None,
    ) -> ResponseT | StreamResponse:
        ...

    def get(
            self,
            path: str,
            *,
            cast_type: Type[ResponseT],
            options: UserRequestInput = {},
            stream: bool = False,
            stream_cls: type[StreamResponse] | None = None,
    ) -> ResponseT | _AsyncStreamT:
        opts = FinalRequestOptions.construct(method="get", url=path, **options)
        return cast(ResponseT, self.request(cast_type, opts, stream=stream, stream_cls=stream_cls))

    @overload
    def post(
            self,
            path: str,
            *,
            cast_type: Type[ResponseT],
            body: Body | None = None,
            options: UserRequestInput = {},
            files: RequestFiles | None = None,
            stream: Literal[False] = False,
    ) -> ResponseT:
        ...

    @overload
    def post(
            self,
            path: str,
            *,
            cast_type: Type[ResponseT],
            body: Body | None = None,
            options: UserRequestInput = {},
            files: RequestFiles | None = None,
            stream: Literal[True],
            stream_cls: type[StreamResponse],
    ) -> StreamResponse:
        ...

    @overload
    def post(
            self,
            path: str,
            *,
            cast_type: Type[ResponseT],
            body: Body | None = None,
            options: UserRequestInput = {},
            files: RequestFiles | None = None,
            stream: bool,
            stream_cls: type[StreamResponse] | None = None,
    ) -> ResponseT | StreamResponse:
        ...

    def post(
            self,
            path: str,
            *,
            cast_type: Type[ResponseT],
            body: Body | None = None,
            options: UserRequestInput = {},
            files: RequestFiles | None = None,
            stream: bool = False,
            stream_cls: type[StreamResponse[Any]] | None = None,
    ) -> ResponseT | StreamResponse:
        opts = FinalRequestOptions.construct(
            method="post", url=path, json_data=body, files=make_httpx_files(files), **options
        )

        return cast(ResponseT,  self.request(cast_type, opts, stream=stream, stream_cls=stream_cls))

    def patch(
            self,
            path: str,
            *,
            cast_type: Type[ResponseT],
            body: Body | None = None,
            options: UserRequestInput = {},
    ) -> ResponseT:
        opts = FinalRequestOptions.construct(method="patch", url=path, json_data=body, **options)

        return self.request(
            cast_type=cast_type, options=opts,
        )

    def put(
            self,
            path: str,
            *,
            cast_type: Type[ResponseT],
            body: Body | None = None,
            options: UserRequestInput = {},
            files: RequestFiles | None = None,
    ) -> ResponseT | StreamResponse:
        opts = FinalRequestOptions.construct(method="put", url=path, json_data=body, files=make_httpx_files(files),
                                            **options)

        return self.request(
            cast_type=cast_type, options=opts,
        )

    def delete(
            self,
            path: str,
            *,
            cast_type: Type[ResponseT],
            body: Body | None = None,
            options: UserRequestInput = {},
    ) -> ResponseT | StreamResponse:
        opts = FinalRequestOptions.construct(method="delete", url=path, json_data=body, **options)

        return self.request(
            cast_type=cast_type, options=opts,
        )

    def _make_status_error(self, response) -> APIStatusError:
        response_text = response.text.strip()
        status_code = response.status_code
        error_msg = f"Error code: {status_code}, with error text {response_text}"

        if status_code == 400:
            return _errors.APIRequestFailedError(message=error_msg, response=response)
        elif status_code == 401:
            return _errors.APIAuthenticationError(message=error_msg, response=response)
        elif status_code == 429:
            return _errors.APIReachLimitError(message=error_msg, response=response)
        elif status_code == 500:
            return _errors.APIInternalError(message=error_msg, response=response)
        elif status_code == 503:
            return _errors.APIServerFlowExceedError(message=error_msg, response=response)
        return APIStatusError(message=error_msg, response=response)


def make_request_options(
        *,
        query: Query | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN
) -> UserRequestInput:
    """Create a dict of type RequestOptions without keys of NotGiven values."""
    options: UserRequestInput = {}
    if extra_headers is not None:
        options["headers"] = extra_headers

    if extra_body is not None:
        options["extra_json"] = cast(AnyMapping, extra_body)

    if query is not None:
        options["params"] = query

    if extra_query is not None:
        options["params"] = {**options.get("params", {}), **extra_query}

    if not isinstance(timeout, NotGiven):
        options["timeout"] = timeout

    return options


def _merge_mappings(
        obj1: Mapping[_T_co, Union[_T, Omit]],
        obj2: Mapping[_T_co, Union[_T, Omit]],
) -> Dict[_T_co, _T]:
    """Merge two mappings of the same type, removing any values that are instances of `Omit`.

    In cases with duplicate keys the second mapping takes precedence.
    """
    merged = {**obj1, **obj2}
    return {key: value for key, value in merged.items() if not isinstance(value, Omit)}
