from typing import TYPE_CHECKING
from .jobs import Jobs
from .models import FineTunedModels
from ...core import BaseAPI

if TYPE_CHECKING:
    from ..._client import ZhipuAI


class FineTuning(BaseAPI):
    jobs: Jobs
    models: FineTunedModels

    def __init__(self, client: "ZhipuAI") -> None:
        super().__init__(client)
        self.jobs = Jobs(client)
        self.models = FineTunedModels(client)

