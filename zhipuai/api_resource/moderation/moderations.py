from __future__ import annotations

from typing import Union, List, TYPE_CHECKING, Dict

import logging
from ...core import BaseAPI, deepcopy_minimal
from ...types.moderation.moderation_completion import Completion


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..._client import ZhipuAI

__all__ = ["Moderations"]
class Moderations(BaseAPI):
    def __init__(self, client: "ZhipuAI") -> None:
        super().__init__(client)

    def create(
            self,
            *,
            model: str,
            input: Union[str, List[str], Dict],
    ) -> Completion:

        body = deepcopy_minimal({
            "model": model,
            "input": input
        })
        return self._post(
            "/moderations",
            body=body,
            cast_type=Completion
        )


