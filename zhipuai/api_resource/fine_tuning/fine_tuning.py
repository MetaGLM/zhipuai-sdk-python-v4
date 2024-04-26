from typing import TYPE_CHECKING
from .jobs import Jobs
from zhipuai.core import BaseAPI

if TYPE_CHECKING:
    from ..._client import ZhipuAI


class FineTuning(BaseAPI):
    jobs: Jobs

    def __init__(self, client: "ZhipuAI") -> None:
        super().__init__(client)
        self.jobs = Jobs(client)

