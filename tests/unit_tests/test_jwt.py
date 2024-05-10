from typing import Iterator

import pytest
import jwt
from zhipuai.core._jwt_token import generate_token

def test_token() -> None:
    # 生成token
    token = generate_token('12345678.abcdefg')
    assert token is not None

    # 解析token
    payload = jwt.decode(token, "abcdefg", algorithms='HS256', options={"verify_signature": False})
    assert payload is not None
    assert payload.get('api_key') == '12345678'

    apikey = "invalid_api_key"
    with pytest.raises(Exception):
        generate_token(apikey)

