from typing import List, TypedDict
from langchain_core.messages import BaseMessage


class Status:
    INVALID_TOOL_USE = "invalid_tool_use"
    COMMON_TOOL_USE = "common_tool_use"
    DELIVERY = "delivery"


class State(TypedDict):
    task: str
    result: str

    messages: List[BaseMessage]
    status: Status
    remaining_reasoning_times: int
