# -*- coding:utf-8 -*-
from __future__ import annotations

import inspect
import warnings
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Type,
    Union,
    Generic,
    Mapping,
    TypeVar,
    Iterable,
    Iterator,
    Optional,
    Generator,
    AsyncIterator,
    cast,
    overload, Literal,
)

import httpx
import pydantic
from httpx import URL, Timeout
from httpx._types import ProxiesTypes

from . import _exceptions
from ._base_models import construct_type, validate_type, FinalRequestOptions
from ._base_type import NotGiven, ResponseT, Body, Headers, NOT_GIVEN, RequestFiles, Query, Data, ModelBuilderProtocol, \
    Transport, RequestOptions
from ._exceptions import (
    APIStatusError,
    APITimeoutError,
    APIConnectionError,
    APIResponseValidationError,
)
from ._files import to_httpx_files
from ._request_opt import ClientRequestParam, UserRequestInput
from ._sse_client import Stream
from .utils import flatten, is_given

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)

_StreamT = TypeVar("_StreamT", bound=Stream[Any])

if TYPE_CHECKING:
    from httpx._config import DEFAULT_TIMEOUT_CONFIG as HTTPX_DEFAULT_TIMEOUT, Limits
else:
    try:
        from httpx._config import DEFAULT_TIMEOUT_CONFIG as HTTPX_DEFAULT_TIMEOUT
    except ImportError:
        # taken from https://github.com/encode/httpx/blob/3ba5fe0d7ac70222590e759c31442b1cab263791/httpx/_config.py#L366
        HTTPX_DEFAULT_TIMEOUT = Timeout(5.0)


def _merge_map(map1: Mapping, map2: Mapping) -> Mapping:
    merged = {**map1, **map2}
    return {key: val for key, val in merged.items() if val is not None}


from httpx._config import DEFAULT_TIMEOUT_CONFIG as HTTPX_DEFAULT_TIMEOUT

ZHIPUAI_DEFAULT_TIMEOUT = httpx.Timeout(timeout=300.0, connect=8.0)
ZHIPUAI_DEFAULT_MAX_RETRIES = 3
ZHIPUAI_DEFAULT_LIMITS = httpx.Limits(max_connections=50, max_keepalive_connections=10)

_HttpxClientT = TypeVar("_HttpxClientT", bound=Union[httpx.Client, httpx.AsyncClient])
_DefaultStreamT = TypeVar("_DefaultStreamT", bound=Union[Stream[Any]])


class BaseClient(Generic[_HttpxClientT, _DefaultStreamT]):
    _client: _HttpxClientT
    _version: str
    _base_url: URL
    max_retries: int
    timeout: Union[float, Timeout, None]
    _limits: httpx.Limits
    _proxies: ProxiesTypes | None
    _transport: Transport | None
    _strict_response_validation: bool
    _idempotency_header: str | None
    _default_stream_cls: type[_DefaultStreamT] | None = None

    def __init__(
            self,
            *,
            version: str,
            base_url: str | URL,
            _strict_response_validation: bool,
            max_retries: int = ZHIPUAI_DEFAULT_MAX_RETRIES,
            timeout: float | Timeout | None = ZHIPUAI_DEFAULT_TIMEOUT,
            limits: httpx.Limits,
            transport: Transport | None,
            proxies: ProxiesTypes | None,
            custom_headers: Mapping[str, str] | None = None,
            custom_query: Mapping[str, object] | None = None,
    ) -> None:

        self._version = version
        self._base_url = self._enforce_trailing_slash(URL(base_url))
        self.max_retries = max_retries
        self.timeout = timeout
        self._limits = limits
        self._proxies = proxies
        self._transport = transport
        self._custom_headers = custom_headers or {}
        self._custom_query = custom_query or {}
        self._strict_response_validation = _strict_response_validation
        self._idempotency_header = None

    def _enforce_trailing_slash(self, url: URL) -> URL:
        if url.raw_path.endswith(b"/"):
            return url
        return url.copy_with(raw_path=url.raw_path + b"/")

    def _make_status_error_from_response(
            self,
            response: httpx.Response,
    ) -> APIStatusError:
        if response.is_closed and not response.is_stream_consumed:
            # We can't read the response body as it has been closed
            # before it was read. This can happen if an event hook
            # raises a status error.
            body = None
            err_msg = f"Error code: {response.status_code}"
        else:
            err_text = response.text.strip()
            body = err_text

            try:
                body = json.loads(err_text)
                err_msg = f"Error code: {response.status_code} - {body}"
            except Exception:
                err_msg = err_text or f"Error code: {response.status_code}"

        return self._make_status_error(err_msg, body=body, response=response)

    def _make_status_error(
            self,
            err_msg: str,
            *,
            body: object,
            response: httpx.Response,
    ) -> _exceptions.APIStatusError:
        raise NotImplementedError()

    def _remaining_retries(
            self,
            remaining_retries: Optional[int],
            options: FinalRequestOptions,
    ) -> int:
        return remaining_retries if remaining_retries is not None else options.get_max_retries(self.max_retries)

    def _build_headers(self, options: FinalRequestOptions) -> httpx.Headers:
        custom_headers = options.headers or {}
        headers_dict = _merge_mappings(self.default_headers, custom_headers)
        self._validate_headers(headers_dict, custom_headers)

        # headers are case-insensitive while dictionaries are not.
        headers = httpx.Headers(headers_dict)

        idempotency_header = self._idempotency_header
        if idempotency_header and options.method.lower() != "get" and idempotency_header not in headers:
            headers[idempotency_header] = options.idempotency_key or self._idempotency_key()

        return headers

    def _prepare_url(self, url: str) -> URL:

        sub_url = URL(url)
        if sub_url.is_relative_url:
            request_raw_url = self._base_url.raw_path + sub_url.raw_path.lstrip(b"/")
            return self._base_url.copy_with(raw_path=request_raw_url)

        return sub_url

    @property
    def default_headers(self):
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
    def auth_headers(self):
        return {}


class SyncHttpxClientWrapper(httpx.Client):
    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass


class SyncAPIClient(BaseClient[httpx.Client, Stream[Any]]):
    _client: httpx.Client
    _default_stream_cls: type[Stream[Any]] | None = None

    def __init__(
            self,
            *,
            version: str,
            base_url: str | URL,
            max_retries: int = ZHIPUAI_DEFAULT_MAX_RETRIES,
            timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
            transport: Transport | None = None,
            proxies: ProxiesTypes | None = None,
            limits: Limits | None = None,
            http_client: httpx.Client | None = None,
            custom_headers: Mapping[str, str] | None = None,
            custom_query: Mapping[str, object] | None = None,
            _strict_response_validation: bool,
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

        if transport is not None:
            warnings.warn(
                "The `transport` argument is deprecated. The `http_client` argument should be passed instead",
                category=DeprecationWarning,
                stacklevel=3,
            )
            if http_client is not None:
                raise ValueError("The `http_client` argument is mutually exclusive with `transport`")

        if proxies is not None:
            warnings.warn(
                "The `proxies` argument is deprecated. The `http_client` argument should be passed instead",
                category=DeprecationWarning,
                stacklevel=3,
            )
            if http_client is not None:
                raise ValueError("The `http_client` argument is mutually exclusive with `proxies`")

        if not is_given(timeout):
            # if the user passed in a custom http client with a non-default
            # timeout set then we use that timeout.
            #
            # note: there is an edge case here where the user passes in a client
            # where they've explicitly set the timeout to match the default timeout
            # as this check is structural, meaning that we'll think they didn't
            # pass in a timeout and will ignore it
            if http_client and http_client.timeout != HTTPX_DEFAULT_TIMEOUT:
                timeout = http_client.timeout
            else:
                timeout = ZHIPUAI_DEFAULT_TIMEOUT

        super().__init__(
            version=version,
            limits=limits,
            # cast to a valid type because mypy doesn't understand our type narrowing
            timeout=cast(Timeout, timeout),
            proxies=proxies,
            base_url=base_url,
            transport=transport,
            max_retries=max_retries,
            custom_query=custom_query,
            custom_headers=custom_headers,
            _strict_response_validation=_strict_response_validation,
        )
        self._client = http_client or SyncHttpxClientWrapper(
            base_url=base_url,
            # cast to a valid type because mypy doesn't understand our type narrowing
            timeout=cast(Timeout, timeout),
            proxies=proxies,
            transport=transport,
            limits=limits,
            follow_redirects=True,
        )

    def is_closed(self) -> bool:
        return self._client.is_closed

    def close(self) -> None:
        """Close the underlying HTTPX client.

        The client will *not* be usable after this.
        """
        # If an error is thrown while constructing a client, self._client
        # may not be present
        if hasattr(self, "_client"):
            self._client.close()

    def __enter__(self: _T) -> _T:
        return self

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def _prepare_request(
            self,
            request_param: ClientRequestParam
    ) -> httpx.Request:
        kwargs: dict[str, Any] = {}
        json_data = request_param.json_data
        headers = self._prepare_headers(request_param)
        url = self._prepare_url(request_param.url)
        json_data = request_param.json_data
        if headers.get("Content-Type") == "multipart/form-data":
            headers.pop("Content-Type")

            if json_data:
                kwargs["data"] = self._make_multipartform(json_data)

        return self._client.build_request(
            headers=headers,
            timeout=self.timeout if isinstance(request_param.timeout, NotGiven) else request_param.timeout,
            method=request_param.method,
            url=url,
            json=json_data,
            files=request_param.files,
            params=request_param.params,
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

    def _process_response_data(
            self,
            *,
            data: object,
            cast_to: type[ResponseT],
            response: httpx.Response,
    ) -> ResponseT:
        if data is None:
            return cast(ResponseT, None)

        if cast_to is object:
            return cast(ResponseT, data)

        try:
            if inspect.isclass(cast_to) and issubclass(cast_to, ModelBuilderProtocol):
                return cast(ResponseT, cast_to.build(response=response, data=data))

            if self._strict_response_validation:
                return cast(ResponseT, validate_type(type_=cast_to, value=data))

            return cast(ResponseT, construct_type(type_=cast_to, value=data))
        except pydantic.ValidationError as err:
            raise APIResponseValidationError(response=response, body=data) from err

    def request(
            self,
            *,
            cast_type: Type[ResponseT],
            params: ClientRequestParam,
            enable_stream: bool = False,
            stream_cls: type[StreamResponse[Any]] | None = None,
    ) -> ResponseT | StreamResponse:
        request = self._prepare_request(params)

        try:
            response = self._client.send(
                request,
                stream=enable_stream,
            )
            response.raise_for_status()
        except httpx.TimeoutException as err:
            raise APITimeoutError(request=request) from err
        except httpx.HTTPStatusError as err:
            err.response.read()
            # raise err
            raise self._make_status_error(err.response) from None

        except Exception as err:
            raise err

        return self._parse_response(
            cast_type=cast_type,
            request_param=params,
            response=response,
            enable_stream=enable_stream,
            stream_cls=stream_cls,
        )

    @overload
    def get(
            self,
            path: str,
            *,
            cast_to: Type[ResponseT],
            options: RequestOptions = {},
            stream: Literal[False] = False,
    ) -> ResponseT:
        ...

    @overload
    def get(
            self,
            path: str,
            *,
            cast_to: Type[ResponseT],
            options: RequestOptions = {},
            stream: Literal[True],
            stream_cls: type[_StreamT],
    ) -> _StreamT:
        ...

    @overload
    def get(
            self,
            path: str,
            *,
            cast_to: Type[ResponseT],
            options: RequestOptions = {},
            stream: bool,
            stream_cls: type[_StreamT] | None = None,
    ) -> ResponseT | _StreamT:
        ...

    def get(
            self,
            path: str,
            *,
            cast_to: Type[ResponseT],
            options: RequestOptions = {},
            stream: bool = False,
            stream_cls: type[_StreamT] | None = None,
    ) -> ResponseT | _StreamT:
        opts = FinalRequestOptions.construct(method="get", url=path, **options)
        # cast is required because mypy complains about returning Any even though
        # it understands the type variables
        return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))

    @overload
    def post(
            self,
            path: str,
            *,
            cast_to: Type[ResponseT],
            body: Body | None = None,
            options: RequestOptions = {},
            files: RequestFiles | None = None,
            stream: Literal[False] = False,
    ) -> ResponseT:
        ...

    @overload
    def post(
            self,
            path: str,
            *,
            cast_to: Type[ResponseT],
            body: Body | None = None,
            options: RequestOptions = {},
            files: RequestFiles | None = None,
            stream: Literal[True],
            stream_cls: type[_StreamT],
    ) -> _StreamT:
        ...

    @overload
    def post(
            self,
            path: str,
            *,
            cast_to: Type[ResponseT],
            body: Body | None = None,
            options: RequestOptions = {},
            files: RequestFiles | None = None,
            stream: bool,
            stream_cls: type[_StreamT] | None = None,
    ) -> ResponseT | _StreamT:
        ...

    def post(
            self,
            path: str,
            *,
            cast_to: Type[ResponseT],
            body: Body | None = None,
            options: RequestOptions = {},
            files: RequestFiles | None = None,
            stream: bool = False,
            stream_cls: type[_StreamT] | None = None,
    ) -> ResponseT | _StreamT:
        opts = FinalRequestOptions.construct(
            method="post", url=path, json_data=body, files=to_httpx_files(files), **options
        )
        return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))

    def patch(
            self,
            path: str,
            *,
            cast_to: Type[ResponseT],
            body: Body | None = None,
            options: RequestOptions = {},
    ) -> ResponseT:
        opts = FinalRequestOptions.construct(method="patch", url=path, json_data=body, **options)
        return self.request(cast_to, opts)

    def put(
            self,
            path: str,
            *,
            cast_to: Type[ResponseT],
            body: Body | None = None,
            files: RequestFiles | None = None,
            options: RequestOptions = {},
    ) -> ResponseT:
        opts = FinalRequestOptions.construct(
            method="put", url=path, json_data=body, files=to_httpx_files(files), **options
        )
        return self.request(cast_to, opts)

    def delete(
            self,
            path: str,
            *,
            cast_to: Type[ResponseT],
            body: Body | None = None,
            options: RequestOptions = {},
    ) -> ResponseT:
        opts = FinalRequestOptions.construct(method="delete", url=path, json_data=body, **options)
        return self.request(cast_to, opts)


def make_user_request_input(
        max_retries: int | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        extra_headers: Headers = None,
        query: Query | None = None,
) -> UserRequestInput:
    options: UserRequestInput = {}

    if extra_headers is not None:
        options["headers"] = extra_headers
    if max_retries is not None:
        options["max_retries"] = max_retries
    if not isinstance(timeout, NotGiven):
        options['timeout'] = timeout
    if query is not None:
        options["params"] = query

    return options
