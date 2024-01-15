from __future__ import annotations

from typing import Union, Any, cast

import pydantic.generics
from httpx import Timeout
from pydantic import ConfigDict
from typing_extensions import (
    final, Unpack, ClassVar, TypedDict

)

from ._base_type import Body, NotGiven, Headers, HttpxRequestFiles, Query
from ._utils import remove_notgiven_indict


class UserRequestInput(TypedDict, total=False):
    max_retries: int
    timeout: float | Timeout | None
    headers: Headers
    params: Query | None


@final
class ClientRequestParam(pydantic.BaseModel):
    method: str
    url: str
    max_retries: Union[int, NotGiven] = NotGiven()
    timeout: Union[float, Timeout, NotGiven] = NotGiven()
    headers: Union[Headers, NotGiven] = NotGiven()
    json_data: Union[Body, None] = None
    files: Union[HttpxRequestFiles, None] = None
    params: Query = {}
    model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)

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
        return cast(ClientRequestParam, super().model_construct(_fields_set, **kwargs))

    model_construct = construct

