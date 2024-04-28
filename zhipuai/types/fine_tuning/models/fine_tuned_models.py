
from typing import List, Union, Optional

from ....core import BaseModel

__all__ = ["FineTunedModelsStatus"]

class FineTunedModelsStatus(BaseModel):
    request_id: str #请求id
    model_name: str #模型名称
    delete_status: str #删除状态 deleting（删除中）, deleted （已删除）