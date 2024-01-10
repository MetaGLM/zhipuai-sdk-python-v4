from pathlib import Path

import anyio
import pytest
from dirty_equals import IsDict, IsList, IsBytes, IsTuple
from zhipuai.core._files import make_httpx_files

readme_path = Path(__file__).parent.parent.parent.joinpath("README.md")


def test_pathlib_includes_file_name() -> None:
    result = make_httpx_files({"file": readme_path})
    print(result)
    assert result == IsDict({"file": IsTuple("README.md", IsBytes())})


def test_tuple_input() -> None:
    result = make_httpx_files([("file", readme_path)])
    print(result)
    assert result == IsList(IsTuple("file", IsTuple("README.md", IsBytes())))


def test_string_not_allowed() -> None:
    with pytest.raises(TypeError, match="Unexpected input file with type <class 'str'>,Expected FileContent type or tuple type"):
        make_httpx_files(
            {
                "file": "foo",  # type: ignore
            }
        )
