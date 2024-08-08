
from typing import Union
from typing_extensions import Annotated, TypeAlias

from .code_interpreter_delta_block import CodeInterpreterToolBlock
from .web_browser_delta_block import WebBrowserToolBlock
from .....core._utils import PropertyInfo
from .drawing_tool_delta_block import DrawingToolBlock

__all__ = ["ToolsType"]


ToolsType: TypeAlias = Annotated[
    Union[DrawingToolBlock, CodeInterpreterToolBlock, WebBrowserToolBlock, RetrievalToolBlock],
    PropertyInfo(discriminator="type"),
]