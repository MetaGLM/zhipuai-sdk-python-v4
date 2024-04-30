from __future__ import annotations

from os import PathLike
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Type,
    Tuple,
    Union,
    Mapping,
    TypeVar,
    Callable,
    Optional,
    Sequence,
)
import pydantic
from httpx import Response
from typing_extensions import Literal, Protocol, TypeAlias, TypedDict, override, runtime_checkable
Query = Mapping[str, object]
Body = object
AnyMapping = Mapping[str, object]
PrimitiveData = Union[str, int, float, bool, None]
Data = Union[PrimitiveData, List[Any], Tuple[Any], "Mapping[str, Any]"]
ModelT = TypeVar("ModelT", bound=pydantic.BaseModel)
_T = TypeVar("_T")

if TYPE_CHECKING:
    NoneType: Type[None]
else:
    NoneType = type(None)


# Sentinel class used until PEP 0661 is accepted
class NotGiven:
    """
    A sentinel singleton class used to distinguish omitted keyword arguments
    from those passed in with the value None (which may have different behavior).

    For example:

    ```py
    def get(timeout: Union[int, NotGiven, None] = NotGiven()) -> Response: ...

    get(timeout=1) # 1s timeout
    get(timeout=None) # No timeout
    get() # Default timeout behavior, which may not be statically known at the method definition.
    ```
    """

    def __bool__(self) -> Literal[False]:
        return False

    @override
    def __repr__(self) -> str:
        return "NOT_GIVEN"


NotGivenOr = Union[_T, NotGiven]
NOT_GIVEN = NotGiven()


class Omit:
    """In certain situations you need to be able to represent a case where a default value has
    to be explicitly removed and `None` is not an appropriate substitute, for example:

    ```py
    # as the default `Content-Type` header is `application/json` that will be sent
    client.post('/upload/files', files={'file': b'my raw file content'})

    # you can't explicitly override the header as it has to be dynamically generated
    # to look something like: 'multipart/form-data; boundary=0d8382fcf5f8c3be01ca2e11002d2983'
    client.post(..., headers={'Content-Type': 'multipart/form-data'})

    # instead you can remove the default `application/json` header by passing Omit
    client.post(..., headers={'Content-Type': Omit()})
    ```
    """

    def __bool__(self) -> Literal[False]:
        return False


@runtime_checkable
class ModelBuilderProtocol(Protocol):
    @classmethod
    def build(
            cls: type[_T],
            *,
            response: Response,
            data: object,
    ) -> _T:
        ...


Headers = Mapping[str, Union[str, Omit]]


class HeadersLikeProtocol(Protocol):
    def get(self, __key: str) -> str | None:
        ...


HeadersLike = Union[Headers, HeadersLikeProtocol]

ResponseT = TypeVar(
    "ResponseT",
    bound="Union[str, None, BaseModel, List[Any], Dict[str, Any], Response, UnknownResponse, ModelBuilderProtocol, BinaryResponseContent]",
)

StrBytesIntFloat = Union[str, bytes, int, float]

# Note: copied from Pydantic
# https://github.com/pydantic/pydantic/blob/32ea570bf96e84234d2992e1ddf40ab8a565925a/pydantic/main.py#L49
IncEx: TypeAlias = "set[int] | set[str] | dict[int, Any] | dict[str, Any] | None"

PostParser = Callable[[Any], Any]


@runtime_checkable
class InheritsGeneric(Protocol):
    """Represents a type that has inherited from `Generic`

    The `__orig_bases__` property can be used to determine the resolved
    type variable for a given base class.
    """

    __orig_bases__: tuple[_GenericAlias]


class _GenericAlias(Protocol):
    __origin__: type[object]


class HttpxSendArgs(TypedDict, total=False):
    auth: httpx.Auth

# for user input files
if TYPE_CHECKING:
    FileContent = Union[IO[bytes], bytes, PathLike[str]]
else:
    FileContent = Union[IO[bytes], bytes, PathLike]

FileTypes = Union[
    FileContent,  # file content
    Tuple[str, FileContent],  # (filename, file)
    Tuple[str, FileContent, str],  # (filename, file , content_type)
    Tuple[str, FileContent, str, Mapping[str, str]],  # (filename, file , content_type, headers)
]

RequestFiles = Union[Mapping[str, FileTypes], Sequence[Tuple[str, FileTypes]]]

# for httpx client supported files

HttpxFileContent = Union[bytes, IO[bytes]]
HttpxFileTypes = Union[
    FileContent,  # file content
    Tuple[str, HttpxFileContent],  # (filename, file)
    Tuple[str, HttpxFileContent, str],  # (filename, file , content_type)
    Tuple[str, HttpxFileContent, str, Mapping[str, str]],  # (filename, file , content_type, headers)
]

HttpxRequestFiles = Union[Mapping[str, HttpxFileTypes], Sequence[Tuple[str, HttpxFileTypes]]]
