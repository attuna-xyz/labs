from typing import Optional, Type

from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from typing import List, Optional
from enum import Enum

class Action(Enum):
    NOTIFY = "NOTIFY"
    RESPOND = "RESPOND"

class DevRelInput(BaseModel):
    tag: str = Field(description="The tag detected in the message")
    sub_tags: List[str] = Field(description="The sub tags detected in the message", default=[])
    message: str = Field(description="The message from the user", default="")

class DevRelOutput(BaseModel):
    action: Action = Field(description="The action to take", default=None)
    message: Optional[str] = Field(description="The message to send", default="")

class ActionGenerator(BaseTool):
    name = "ACTION_GENERATOR"
    description = "Always call this tool at the end to generate an action in appropriate format"
    args_schema: Type[BaseModel] = DevRelOutput
    
    def _run(
        self, action: Action, message: Optional[str], run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """"""
        return DevRelOutput(action=action, message=message)