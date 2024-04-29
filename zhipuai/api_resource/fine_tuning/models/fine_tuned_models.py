from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import httpx

from ....core import BaseAPI
from ....core import NOT_GIVEN, Headers, NotGiven, Body
from ....core import (
    make_request_options,
)

from ....types.fine_tuning.models import (
    FineTunedModelsStatus
)

if TYPE_CHECKING:
    from ...._client import ZhipuAI

__all__ = ["FineTunedModels"]


class FineTunedModels(BaseAPI):

    def __init__(self, client: "ZhipuAI") -> None:
        super().__init__(client)

    def delete(
            self,
            fine_tuned_model: str,
            *,
            extra_headers: Headers | None = None,
            extra_query: Query | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FineTunedModelsStatus:

        if not fine_tuning_job_id:
            raise ValueError(f"Expected a non-empty value for `fine_tuning_job_id` but received {fine_tuning_job_id!r}")
        return self._delete(
            f"fine_tuning/fine_tuned_models/{fine_tuned_model}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_type=FineTunedModelsStatus,
        )