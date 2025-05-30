from typing import TYPE_CHECKING

from .moderations import Moderations
from ...core import BaseAPI, cached_property

__all__ = ["Moderation"]
class Moderation(BaseAPI):
    @cached_property
    def moderations(self) -> Moderations:
        return Moderations(self._client)