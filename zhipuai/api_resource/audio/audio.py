from __future__ import annotations

from ...core import BaseAPI, cached_property
from .transcriptions import Transcriptions



__all__ = ["Audio"]
class Audio(BaseAPI):
    @cached_property
    def transcriptions(self) -> Transcriptions:
        return Transcriptions(self._client)
