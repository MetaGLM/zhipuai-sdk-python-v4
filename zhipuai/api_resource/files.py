from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import typing_extensions

from ..core import BaseAPI
from ..core import NOT_GIVEN, Body, Query, Headers, NotGiven, FileTypes
from ..core import is_file_content

from ..core import (
    make_request_options,
)
from ..types.file_object import FileObject, ListOfFileObject

from ..core import _legacy_response

if TYPE_CHECKING:
    from .._client import ZhipuAI

__all__ = ["Files"]


class Files(BaseAPI):

    def __init__(self, client: "ZhipuAI") -> None:
        super().__init__(client)

    def create(
            self,
            *,
            file: FileTypes,
            purpose: str,
            extra_headers: Headers | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileObject:
        if not is_file_content(file):
            prefix = f"Expected file input `{file!r}`"
            raise RuntimeError(
                f"{prefix} to be bytes, an io.IOBase instance, PathLike or a tuple but received {type(file)} instead."
            ) from None
        files = [("file", file)]

        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}

        return self._post(
            "/files",
            body={
                "purpose": purpose,
            },
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_body=extra_body, timeout=timeout
            ),
            cast_type=FileObject,
        )

    def list(
            self,
            *,
            purpose: str | NotGiven = NOT_GIVEN,
            limit: int | NotGiven = NOT_GIVEN,
            after: str | NotGiven = NOT_GIVEN,
            order: str | NotGiven = NOT_GIVEN,
            extra_headers: Headers | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListOfFileObject:
        return self._get(
            "/files",
            cast_type=ListOfFileObject,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "purpose": purpose,
                    "limit": limit,
                    "after": after,
                    "order": order,
                },
            ),
        )

    def content(
            self,
            file_id: str,
            *,
            extra_headers: Headers | None = None,
            extra_query: Query | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> _legacy_response.HttpxBinaryResponseContent:
        """
        Returns the contents of the specified file.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        extra_headers = {"Accept": "application/binary", **(extra_headers or {})}
        return self._get(
            f"/files/{file_id}/content",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_type=_legacy_response.HttpxBinaryResponseContent,
        )

    @typing_extensions.deprecated("The `.content()` method should be used instead")
    def retrieve_content(
            self,
            file_id: str,
            *,
            extra_headers: Headers | None = None,
            extra_query: Query | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Returns the contents of the specified file.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return self._get(
            f"/files/{file_id}/content",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_type=str,
        )
