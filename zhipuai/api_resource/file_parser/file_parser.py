from __future__ import annotations

from typing import TYPE_CHECKING, Mapping, cast

import httpx
from typing_extensions import Literal

from ...core import BaseAPI, maybe_transform
from ...core import NOT_GIVEN, Body, Headers, NotGiven, FileTypes
from ...core import _legacy_binary_response
from ...core import _legacy_response
from ...core import deepcopy_minimal, extract_files
from ...core import (
    make_request_options,
)
from ...types.file_parser.file_parser_create_params import FileParserCreateParams
from ...types.file_parser.file_parser_resp import FileParserTaskCreateResp

if TYPE_CHECKING:
    from ..._client import ZhipuAI

__all__ = ["FileParser"]


class FileParser(BaseAPI):

    def __init__(self, client: "ZhipuAI") -> None:
        super().__init__(client)

    def create(
            self,
            *,
            file: FileTypes = None,
            file_type: str = None,
            tool_type: Literal["simple", "doc2x", "tencent", "zhipu-pro"],
            extra_headers: Headers | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileParserTaskCreateResp:

        if not file:
            raise ValueError("At least one `file` must be provided.")
        body = deepcopy_minimal(
            {
                "file": file,
                "file_type": file_type,
                "tool_type": tool_type,
            }
        )

        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        if files:
            # It should be noted that the actual Content-Type header that will be
            # sent to the server will contain a `boundary` parameter, e.g.
            # multipart/form-data; boundary=---abc--
            extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/files/parser/create",
            body=maybe_transform(body, FileParserCreateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_body=extra_body, timeout=timeout
            ),
            cast_type=FileParserTaskCreateResp,
        )

    def content(
            self,
            task_id: str,
            *,
            format_type: Literal["text", "download_link"],
            extra_headers: Headers | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> _legacy_response.HttpxBinaryResponseContent:
        """
        Returns the contents of the specified file.

        Args:
          extra_headers: Send extra headers

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        extra_headers = {"Accept": "application/binary", **(extra_headers or {})}
        return self._get(
            f"/files/parser/result/{task_id}/{format_type}",
            options=make_request_options(
                extra_headers=extra_headers, extra_body=extra_body, timeout=timeout
            ),
            cast_type=_legacy_binary_response.HttpxBinaryResponseContent,
        )
