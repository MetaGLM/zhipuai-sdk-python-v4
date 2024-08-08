from typing import List

from typing_extensions import Literal

from .....core import BaseModel


class RetrievalToolOutput(BaseModel):
    text: str
    document: str


class RetrievalTool(BaseModel):

    outputs: List[RetrievalToolOutput]


class RetrievalToolBlock(BaseModel):
    retrieval: RetrievalTool

    type: Literal["retrieval"]
    """Always `retrieval`."""
