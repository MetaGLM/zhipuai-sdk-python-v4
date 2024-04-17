# -*- coding:utf-8 -*-
from __future__ import annotations

import json
import json
import inspect
from types import TracebackType
from typing import TYPE_CHECKING, Any, Generic, TypeVar, Iterator, AsyncIterator, cast
from typing_extensions import Self, TypeGuard, override, get_origin
import httpx

from .utils import is_mapping, extract_type_var_from_base
from ._exceptions import APIError

_FIELD_SEPARATOR = ":"

if TYPE_CHECKING:
    from .._client import ZhipuAI

_T = TypeVar("_T")


class Stream(Generic[_T]):
    """Provides the core interface to iterate over a synchronous stream response."""

    response: httpx.Response

    def __init__(
            self,
            *,
            cast_to: type[_T],
            response: httpx.Response,
            client: ZhipuAI,
    ) -> None:
        self.response = response
        self._cast_to = cast_to
        self._client = client
        self._decoder = SSEDecoder()
        self._iterator = self.__stream__()

    def __next__(self) -> _T:
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[_T]:
        for item in self._iterator:
            yield item

    def _iter_events(self) -> Iterator[Event]:
        yield from self._decoder.iter(self.response.iter_lines())

    def __stream__(self) -> Iterator[_T]:
        cast_to = cast(Any, self._cast_to)
        response = self.response
        process_data = self._client._process_response_data
        iterator = self._iter_events()

        for sse in iterator:
            if sse.data.startswith("[DONE]"):
                break

            if sse.event is None:
                data = sse.json()
                if is_mapping(data) and data.get("error"):
                    raise APIError(
                        message="An error occurred during streaming",
                        request=self.response.request,
                        body=data["error"],
                    )

                yield process_data(data=data, cast_to=cast_to, response=response)

        # Ensure the entire stream is consumed
        for _sse in iterator:
            ...

    def __enter__(self) -> Self:
        return self

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        """
        Close the response and release the connection.

        Automatically called if the response body is read to completion.
        """
        self.response.close()


class Event(object):
    def __init__(
            self,
            *,
            event: str | None = None,
            data: str | None = None,
            id: str | None = None,
            retry: int | None = None
    ):
        self._event = event
        self._data = data
        self._id = id
        self._retry = retry

    def __repr__(self):
        data_len = len(self._data) if self._data else 0
        return f"Event(event={self._event}, data={self._data} ,data_length={data_len}, id={self._id}, retry={self._retry}"

    @property
    def event(self): return self._event

    @property
    def data(self): return self._data

    def json(self) -> Any:
        return json.loads(self.data)

    @property
    def id(self): return self._id

    @property
    def retry(self): return self._retry


class SSEDecoder:
    _data: list[str]
    _event: str | None
    _retry: int | None
    _last_event_id: str | None

    def __init__(self) -> None:
        self._event = None
        self._data = []
        self._last_event_id = None
        self._retry = None

    def iter(self, iterator: Iterator[str]) -> Iterator[Event]:
        """Given an iterator that yields lines, iterate over it & yield every event encountered"""
        for line in iterator:
            line = line.rstrip("\n")
            sse = self.decode(line)
            if sse is not None:
                yield sse

    async def aiter(self, iterator: AsyncIterator[str]) -> AsyncIterator[Event]:
        """Given an async iterator that yields lines, iterate over it & yield every event encountered"""
        async for line in iterator:
            line = line.rstrip("\n")
            sse = self.decode(line)
            if sse is not None:
                yield sse

    def decode(self, line: str) -> Event | None:
        # See: https://html.spec.whatwg.org/multipage/server-sent-events.html#event-stream-interpretation  # noqa: E501

        if not line:
            if not self._event and not self._data and not self._last_event_id and self._retry is None:
                return None

            sse = Event(
                event=self._event,
                data="\n".join(self._data),
                id=self._last_event_id,
                retry=self._retry,
            )

            # NOTE: as per the SSE spec, do not reset last_event_id.
            self._event = None
            self._data = []
            self._retry = None

            return sse

        if line.startswith(":"):
            return None

        fieldname, _, value = line.partition(":")

        if value.startswith(" "):
            value = value[1:]

        if fieldname == "event":
            self._event = value
        elif fieldname == "data":
            self._data.append(value)
        elif fieldname == "id":
            if "\0" in value:
                pass
            else:
                self._last_event_id = value
        elif fieldname == "retry":
            try:
                self._retry = int(value)
            except (TypeError, ValueError):
                pass
        else:
            pass  # Field is ignored.

        return None


def is_stream_class_type(typ: type) -> TypeGuard[type[Stream[object]]]:
    """TypeGuard for determining whether or not the given type is a subclass of `Stream` / `AsyncStream`"""
    origin = get_origin(typ) or typ
    return inspect.isclass(origin) and issubclass(origin, Stream)


def extract_stream_chunk_type(
        stream_cls: type,
        *,
        failure_message: str | None = None,
) -> type:
    """Given a type like `Stream[T]`, returns the generic type variable `T`.

    This also handles the case where a concrete subclass is given, e.g.
    ```py
    class MyStream(Stream[bytes]):
        ...

    extract_stream_chunk_type(MyStream) -> bytes
    ```
    """
    return extract_type_var_from_base(
        stream_cls,
        index=0,
        generic_bases=cast("tuple[type, ...]", Stream),
        failure_message=failure_message,
    )
