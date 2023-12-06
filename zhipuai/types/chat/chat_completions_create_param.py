from typing import List, Optional, TypedDict
from typing_extensions import Literal
from pydantic import BaseModel


class Reference(TypedDict, total=False):
    enable: Optional[bool]
    search_query: Optional[str]
