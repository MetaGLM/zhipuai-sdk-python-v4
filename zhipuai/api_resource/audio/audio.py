from __future__ import annotations

from ...core import BaseAPI, cached_property
from .transcriptions import Transcriptions

class Audio(BaseAPI):
    @cached_property
    def transcriptions(self) -> Transcriptions:
        return Transcriptions(self._client)
