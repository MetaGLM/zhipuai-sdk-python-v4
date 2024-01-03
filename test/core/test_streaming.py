from typing import Iterator

import pytest

from zhipuai.core._sse_client import SSELineParser


def test_basic() -> None:
    def body() -> Iterator[str]:
        yield "event: completion"
        yield 'data: {"foo":true}'
        yield ""

    it = SSELineParser().iter_lines(body())
    sse = next(it)
    assert sse.event == "completion"
    assert sse.json_data() == {"foo": True}

    with pytest.raises(StopIteration):
        next(it)


def test_data_missing_event() -> None:
    def body() -> Iterator[str]:
        yield 'data: {"foo":true}'
        yield ""

    it = SSELineParser().iter_lines(body())
    sse = next(it)
    assert sse.event is None
    assert sse.json_data() == {"foo": True}

    with pytest.raises(StopIteration):
        next(it)


def test_event_missing_data() -> None:
    def body() -> Iterator[str]:
        yield "event: ping"
        yield ""

    it = SSELineParser().iter_lines(body())
    sse = next(it)
    assert sse.event == "ping"
    assert sse.data == ""

    with pytest.raises(StopIteration):
        next(it)


def test_multiple_events() -> None:
    def body() -> Iterator[str]:
        yield "event: ping"
        yield ""
        yield "event: completion"
        yield ""

    it = SSELineParser().iter_lines(body())

    sse = next(it)
    assert sse.event == "ping"
    assert sse.data == ""

    sse = next(it)
    assert sse.event == "completion"
    assert sse.data == ""

    with pytest.raises(StopIteration):
        next(it)


def test_multiple_events_with_data() -> None:
    def body() -> Iterator[str]:
        yield "event: ping"
        yield 'data: {"foo":true}'
        yield ""
        yield "event: completion"
        yield 'data: {"bar":false}'
        yield ""

    it = SSELineParser().iter_lines(body())

    sse = next(it)
    assert sse.event == "ping"
    assert sse.json_data() == {"foo": True}

    sse = next(it)
    assert sse.event == "completion"
    assert sse.json_data() == {"bar": False}

    with pytest.raises(StopIteration):
        next(it)
