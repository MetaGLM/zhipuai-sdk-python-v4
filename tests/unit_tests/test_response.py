import httpx
from httpx import URL, ByteStream, Headers, Request, Response
from typing_extensions import Dict, Type

from zhipuai.core import StreamResponse
from zhipuai.core._base_type import ResponseT
from zhipuai.core._http_client import HttpClient
from zhipuai.core._request_opt import FinalRequestOptions
from zhipuai.core._response import APIResponse


# Mock objects for HttpClient and StreamResponse if necessary
class MockHttpClient:
	_strict_response_validation: bool = False

	# Implement necessary mock methods or attributes
	def _process_response_data(
		self,
		*,
		data: object,
		cast_type: Type[ResponseT],
		response: httpx.Response,
	) -> ResponseT:
		return data


class MockStreamResponse(StreamResponse[ResponseT]):
	# Implement necessary mock methods or attributes
	def __init__(
		self,
		*,
		cast_type: Type[ResponseT],
		response: httpx.Response,
		client: HttpClient,
	) -> None:
		super().__init__(cast_type=cast_type, response=response, client=client)
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
	opts = FinalRequestOptions.construct(method='get', url='path')
	http_response = APIResponse(
		raw=raw_response,
		cast_type=str,
		client=MockHttpClient(),
		stream=False,
		options=opts,
	)
	assert http_response.http_response == raw_response


# Test parse Method
def test_parse_method():
	raw_response = Response(
		200,
		headers=Headers({'content-type': 'application/json'}),
		content=b'{"key": "value"}',
	)
	opts = FinalRequestOptions.construct(method='get', url='path')

	http_response = APIResponse(
		raw=raw_response,
		cast_type=Dict[str, object],
		client=MockHttpClient(),
		stream=False,
		options=opts,
	)
	parsed_data = http_response.parse()
	assert parsed_data == {'key': 'value'}
	http_response = APIResponse(
		raw=raw_response,
		cast_type=str,
		client=MockHttpClient(),
		stream=False,
		options=opts,
	)
	parsed_data = http_response.parse()
	assert parsed_data == '{"key": "value"}'

	raw_response = Response(
		200,
		content=b'{"key": "value"}',
		stream=ByteStream(b'{"key": "value"}\n"foo"\n"boo"\n'),
	)
	http_response = APIResponse(
		raw=raw_response,
		cast_type=str,
		client=MockHttpClient(),
		stream=True,
		options=opts,
		stream_cls=MockStreamResponse[str],
	)
	parsed_data = http_response.parse()
	excepted_data = ['{"key": "value"}', '"foo"', '"boo"']
	data = [chunk.strip() for chunk in parsed_data]
	assert data == excepted_data


# Test properties
def test_properties():
	opts = FinalRequestOptions.construct(method='get', url='path')
	headers = Headers({'content-type': 'application/json'})
	request = Request(method='GET', url='http://example.com')
	raw_response = Response(200, headers=headers, request=request)
	http_response = APIResponse(
		raw=raw_response,
		cast_type=str,
		client=MockHttpClient(),
		stream=False,
		options=opts,
	)

	assert http_response.headers == headers
	assert http_response.http_request == request
	assert http_response.status_code == 200
	assert http_response.url == URL('http://example.com')
	assert http_response.method == 'GET'
