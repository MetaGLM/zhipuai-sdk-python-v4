from typing import List, Union, Optional
from typing_extensions import Literal

from pydantic import BaseModel

__all__ = ["FineTuningJob", "Error", "Hyperparameters"]


class Error(BaseModel):
    code: str
    message: str
    param: Optional[str] = None


class Hyperparameters(BaseModel):
    n_epochs: Union[Literal["auto"], int]


class FineTuningJob(BaseModel):
    id: str

    created_at: int

    error: Optional[Error] = None

    fine_tuned_model: Optional[str] = None

    finished_at: Optional[int] = None

    hyperparameters: Hyperparameters

    model: str

    object: str

    organization_id: str

    result_files: List[str]

    status: str

    trained_tokens: Optional[int] = None

    training_file: str

    validation_file: Optional[str] = None
