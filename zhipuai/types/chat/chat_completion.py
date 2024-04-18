from typing import List, Optional, Union, Dict, Any

from pydantic import BaseModel, ConfigDict, Field, Extra, root_validator, model_validator

__all__ = ["Completion", "CompletionUsage"]

from zhipuai.core._base_type import AnyMapping


class Function(BaseModel):
    arguments: str
    name: str


class CompletionMessageToolCall(BaseModel):
    id: str
    function: Function
    type: str


class CompletionMessage(BaseModel):
    content: Optional[str] = None
    role: str
    tool_calls: Optional[List[CompletionMessageToolCall]] = None


class CompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionChoice(BaseModel):
    index: int
    finish_reason: str
    message: CompletionMessage


class Completion(BaseModel):
    # model_config = ConfigDict(extra='allow')
    model: Optional[str] = None
    created: Optional[int] = None
    choices: List[CompletionChoice]
    request_id: Optional[str] = None
    id: Optional[str] = None
    usage: CompletionUsage
    extra_json: Dict[str, Any]

    @root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        all_required_field_names = {field for field in cls.__fields__.keys() if field != 'extra_json'}  # to support alias
        extra: Dict[str, Any] = {}
        for field_name in list(values):
            if field_name not in all_required_field_names:
                extra[field_name] = values.pop(field_name)
        values['extra_json'] = extra
        return values
