from typing import List, Optional, Union, Dict

from ...core import BaseModel

__all__ = ["Completion"]

class Completion(BaseModel):
    model: Optional[str] = None
    input: Optional[Union[str, List[str], Dict]] = None  # 新增 input 字段


