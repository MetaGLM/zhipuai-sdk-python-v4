from typing import Optional

from pydantic import BaseModel

__all__ = ["FileObject"]


class FileObject(BaseModel):

    id: str
    bytes: int
    created_at: int
    filename: str
    object: str
    purpose: str
    status: str
    status_details: Optional[str] = None

