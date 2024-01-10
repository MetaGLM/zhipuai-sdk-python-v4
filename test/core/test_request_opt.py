import pytest
from httpx import Timeout
from zhipuai.core._request_opt import ClientRequestParam, NotGiven

# Test Initialization and Default Values
def test_initialization():
    params = ClientRequestParam(method="GET", url="http://example.com")
    assert isinstance(params.max_retries, NotGiven)
    assert isinstance(params.timeout, NotGiven)
    assert isinstance(params.headers, NotGiven)
    assert params.json_data is None

# Test get_max_retries Method
@pytest.mark.parametrize("max_retries_input, expected", [
    (NotGiven(), 5),  # Default case
    (3, 3),           # Specific number
])
def test_get_max_retries(max_retries_input, expected):
    params = ClientRequestParam(method="GET", url="http://example.com", max_retries=max_retries_input)
    assert params.get_max_retries(5) == expected

# Test construct Method
def test_construct():
    input_data = {
        "max_retries": 3,
        "timeout": 10.0,
        "headers": {"Content-Type": "application/json"}
    }
    params = ClientRequestParam.construct(**input_data)
    assert params.max_retries == input_data["max_retries"]
    assert params.timeout == input_data["timeout"]
    assert params.headers == input_data["headers"]
