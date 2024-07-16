from __future__ import annotations

import os

import httpx
import pytest
from respx import MockRouter

from zhipuai import ZhipuAI
from zhipuai.api_resource import FilesWithRawResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:2333")
api_key = "Key.secret"


class TestZhipuAIFile:
    client = ZhipuAI(base_url=base_url, api_key=api_key)

    @pytest.mark.respx(base_url=base_url)
    def test_file_download_jsonl_raises(self, test_file_path: str, respx_mock: MockRouter) -> None:
        with open(os.path.join(test_file_path, "batchinput.jsonl"), "rb") as file:
            respx_mock.get("/files/1/content").mock(
                return_value=httpx.Response(200, content=file.read())
            )
        legacy = FilesWithRawResponse(self.client.files)
        response = legacy.content("1")
        files_content = response.parse()

        assert files_content.content == b'{"custom_id": "request-1", "method": "POST", "url": "/v4/chat/completions", "body": {"model": "glm-4", "messages": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}'
        with pytest.raises(NotImplementedError) as exc:
            files_content.json()
        assert exc.type == NotImplementedError

    @pytest.mark.respx(base_url=base_url)
    def test_file_download_jsonl(self, test_file_path: str, respx_mock: MockRouter) -> None:
        with open(os.path.join(test_file_path, "batchinput.jsonl"), "rb") as file:
            respx_mock.get("/files/1/content").mock(
                return_value=httpx.Response(200, content=file.read(),
                                            headers={
                                                "Content-Type": "application/jsonl",
                                                "Content-Disposition": "attachment; filename=batchinput.jsonl"
                                            }
                                            )
            )
        legacy = FilesWithRawResponse(self.client.files)
        response = legacy.content("1")
        files_content = response.parse()

        assert files_content.content == b'{"custom_id": "request-1", "method": "POST", "url": "/v4/chat/completions", "body": {"model": "glm-4", "messages": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}'

        text = next(files_content.iter_text())
        assert text == '{"custom_id": "request-1", "method": "POST", "url": "/v4/chat/completions", "body": {"model": "glm-4", "messages": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}'
 

    def test_is_closed(self):
        assert self.client.is_closed() is False

    def test_close(self):
        self.client.close()
        assert self.client.is_closed() is True
