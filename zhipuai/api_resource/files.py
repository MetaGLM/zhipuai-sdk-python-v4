from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from ..core import BaseAPI
from ..core import NOT_GIVEN, Body, Query, Headers, NotGiven, FileTypes
from ..core import is_file_content
from ..core import (
    make_request_options,
)
from ..types.file_object import FileObject, ListOfFileObject

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
