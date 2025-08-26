from agents.planner.schema import Status, State
from agents.response import Response
from agents.worker.external import call_workers
import logging


class ToolExecuteResult:
    def __init__(
        self,
        content: str = "",
    ):
        self.content: str = content


from agents.planner.schema import State
from agents.tool_content_parser import ToolUse


def tool_use_title_generator(tool: ToolUse) -> str:
    return f"[result for tool {tool['name']}]"


async def execute_tool(state: State, tool: ToolUse) -> tuple[ToolExecuteResult, State]:
    tool_execute_result, state_updates = await execute_tool_inner(state, tool)

    tool_execute_result.content = f"""
    {tool_use_title_generator(tool)}
    {tool_execute_result.content}
    """
    return tool_execute_result, state_updates


async def execute_tool_inner(
    state: State, tool: ToolUse
) -> tuple[ToolExecuteResult, State]:
    """
    return ToolExecuteResult, state_updates
    """

    tool_execute_result = ToolExecuteResult()
    state_updates = {}

    match tool["name"]:
        case "dispatch_tasks":
            if "subtasks" not in tool["params"]:
                state_updates["status"] = Status.INVALID_TOOL_USE
                tool_execute_result.content = Response.missingParam(
                    "dispatch_tasks", ["subtasks"]
                )
                return tool_execute_result, state_updates

            subtasks = []
            subtasks = tool["params"]["subtasks"].split("\n")
            subtasks = [subtask.strip() for subtask in subtasks]

            try:
                workers_result = await call_workers(subtasks)
            except Exception as e:
                logging.error(f"failed to call workers: {e}")
                state_updates["status"] = Status.INVALID_TOOL_USE
                tool_execute_result.content = (
                    "[Error] Unknown runtime error in tool operation."
                )
                return tool_execute_result, state_updates
            tool_execute_result.content = workers_result
            state_updates["status"] = Status.COMMON_TOOL_USE
            return tool_execute_result, state_updates

        case "deliver_report":
            if "content" not in tool["params"]:
                state_updates["status"] = Status.INVALID_TOOL_USE
                tool_execute_result.content = Response.missingParam(
                    "deliver_report", ["content"]
                )
                return tool_execute_result, state_updates
            state_updates["result"] = tool["params"]["content"].strip()
            state_updates["status"] = Status.DELIVERY
            return tool_execute_result, state_updates
