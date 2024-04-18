from __future__ import annotations

from typing import Union, Any, cast, TYPE_CHECKING

from ._base_compat import ConfigDict, PYDANTIC_V2
import pydantic.generics
from httpx import Timeout
from typing_extensions import (
    final, Unpack, ClassVar, TypedDict

)

from ._base_type import Body, NotGiven, Headers, HttpxRequestFiles, Query, AnyMapping
from ._utils import remove_notgiven_indict, strip_not_given


class UserRequestInput(TypedDict, total=False):
    headers: Headers
    max_retries: int
    timeout: float | Timeout | None
    params: Query
    extra_json: AnyMapping


@final
class ClientRequestParam(pydantic.BaseModel):
    method: str
    url: str
    max_retries: Union[int, NotGiven] = NotGiven()
    timeout: Union[float, Timeout, NotGiven] = NotGiven()
    headers: Union[Headers, NotGiven] = NotGiven()
    files: Union[HttpxRequestFiles, None] = None
    params: Query = {}

    json_data: Union[Body, None] = None
    extra_json: Union[AnyMapping, None] = None

    if PYDANTIC_V2:
        model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)
    else:

        class Config(pydantic.BaseConfig):  # pyright: ignore[reportDeprecated]
            arbitrary_types_allowed: bool = True

    def get_max_retries(self, max_retries) -> int:
        if isinstance(self.max_retries, NotGiven):
            return max_retries
        return self.max_retries

    @classmethod
    def construct(  # type: ignore
            cls,
            _fields_set: set[str] | None = None,
            **values: Unpack[UserRequestInput],
    ) -> ClientRequestParam :
        kwargs: dict[str, Any] = {
            key: remove_notgiven_indict(value) for key, value in values.items()
        }
        kwargs: dict[str, Any] = {
            # we unconditionally call `strip_not_given` on any value
            # as it will just ignore any non-mapping types
            key: strip_not_given(value)
            for key, value in values.items()
        }
        if PYDANTIC_V2:
            return cast(ClientRequestParam, super().model_construct(_fields_set, **kwargs))

        return cast(ClientRequestParam, super().construct(_fields_set, **kwargs))  # pyright: ignore[reportDeprecated]

    if not TYPE_CHECKING:
        # type checkers incorrectly complain about this assignment
        model_construct = construct
