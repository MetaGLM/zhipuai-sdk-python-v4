import httpx
import pytest
from httpx import Response, Request, Headers, URL, ByteStream
import datetime

from typing_extensions import Generic

from zhipuai.core._sse_client import StreamResponse

from zhipuai.core._base_type import ResponseT

from zhipuai.core._response import HttpResponse
from zhipuai.core._http_client import HttpClient


# Mock objects for HttpClient and StreamResponse if necessary
class MockHttpClient:
    # Implement necessary mock methods or attributes
    def _process_response_data(
            self,
            *,
            data: object,
            cast_type: type[ResponseT],
            response: httpx.Response,
    ) -> ResponseT:
        return data


class MockStreamResponse(Generic[ResponseT]):
    # Implement necessary mock methods or attributes
    def __init__(
            self,
            *,
            cast_type: type[ResponseT],
            response: httpx.Response,
            client: HttpClient,
    ) -> None:
        self.response = response
        self._cast_type = cast_type
        # self._data_process_func = client._process_response_data
        # self._strem_chunks = self.__stream__()

    def __iter__(self):
        for item in self.response.iter_lines():
            yield item


# Test Initialization
def test_http_response_initialization():
    raw_response = Response(200)
    http_response = HttpResponse(raw_response=raw_response, cast_type=str, client=MockHttpClient())
    assert http_response.http_response == raw_response


# Test parse Method
def test_parse_method():
    raw_response = Response(200, content=b'{"key": "value"}')
    http_response = HttpResponse(raw_response=raw_response, cast_type=dict, client=MockHttpClient())
    parsed_data = http_response.parse()
    assert parsed_data == {"key": "value"}
    http_response = HttpResponse(raw_response=raw_response, cast_type=str, client=MockHttpClient())
    parsed_data = http_response.parse()
    assert parsed_data == '{"key": "value"}'

    raw_response = Response(200, content=b'{"key": "value"}', stream=ByteStream(b'{"key": "value"}\n"foo"\n"boo"\n'))
    http_response = HttpResponse(raw_response=raw_response, cast_type=str, client=MockHttpClient(), enable_stream=True,
                                 stream_cls=MockStreamResponse[str])
    parsed_data = http_response.parse()
    excepted_data = ['{"key": "value"}', '"foo"', '"boo"']
    data = [chunk.strip() for chunk in parsed_data]
    assert data == excepted_data


# Test properties
def test_properties():
    headers = Headers({"content-type": "application/json"})
    request = Request(method="GET", url="http://example.com")
    raw_response = Response(200, headers=headers, request=request)
    http_response = HttpResponse(raw_response=raw_response, cast_type=str, client=MockHttpClient())

    assert http_response.headers == headers
    assert http_response.http_request == request
    assert http_response.status_code == 200
    assert http_response.url == URL("http://example.com")
    assert http_response.method == "GET"
