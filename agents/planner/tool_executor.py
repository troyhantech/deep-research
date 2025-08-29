from agents.planner.schema import Status, State
from agents.response import Response
from agents.worker.external import call_workers
import logging
from agents.reporter.agent import generate_report


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

    tool_execute_result.content = f"""{tool_use_title_generator(tool)}
{tool_execute_result.content}"""
    return tool_execute_result, state_updates


async def execute_tool_inner(
    state: State, tool: ToolUse
) -> tuple[ToolExecuteResult, State]:
    """
    return ToolExecuteResult, state_updates
    """
    config = state["config"]

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
            subtasks = tool["params"]["subtasks"].strip().split("\n")
            subtasks = [subtask.strip() for subtask in subtasks]

            # only keep the first n subtasks
            subtasks = subtasks[: config["planner"].get("max_subtasks", 10)]

            try:
                workers_result = await call_workers(subtasks, config)
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

        case "generate_report":
            messages = state["messages"]

            # remove the system message
            messages = messages[1:]

            context = "\n\n".join([f"{msg.type}: {msg.content}" for msg in messages])
            info = f"""<context>
{context}
</context>"""

            report = await generate_report(info, state["task"], config)
            state_updates["result"] = report
            state_updates["status"] = Status.GENERATE_REPORT
            return tool_execute_result, state_updates
