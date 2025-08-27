import logging, json

from mcp import ClientSession
from agents.worker.schema import Status, State
from agents.response import Response
from agents.reporter.agent import generate_report


class ToolExecuteResult:
    def __init__(
        self,
        content: str = "",
    ):
        self.content: str = content


from agents.worker.schema import State
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

    tool_execute_result = ToolExecuteResult()
    state_updates = {}

    match tool["name"]:
        case "call_mcp_tool":
            # 校验参数
            server_name = tool["params"].get("server_name", "")
            tool_name = tool["params"].get("tool_name", "")
            arguments = tool["params"].get("arguments", "")

            missing_params = []
            if not server_name:
                missing_params.append("server_name")
            if not tool_name:
                missing_params.append("tool_name")

            if missing_params:
                state_updates["status"] = Status.INVALID_TOOL_USE
                tool_execute_result.content = Response.missingParam(
                    "call_mcp_tool", missing_params
                )
                return tool_execute_result, state_updates

            try:
                arguments = json.loads(arguments)
            except Exception as e:
                logging.warning(
                    f"arguments is not a valid json string, arguments: {arguments}, error: {e}"
                )
                state_updates["status"] = Status.INVALID_TOOL_USE
                tool_execute_result.content = f"[Error] arguments is not a valid json string, arguments: {arguments}, error: {e}"
                return tool_execute_result, state_updates

            from pkg.mcp.mcp_hub import mcp_hub

            connection = mcp_hub.connections.get(server_name)

            if not connection:
                state_updates["status"] = Status.INVALID_TOOL_USE
                tool_execute_result.content = (
                    f"[Error] server_name {server_name} not found."
                )
                return tool_execute_result, state_updates

            try:
                from pkg.mcp.types import McpServerType

                if connection.server.config.type == McpServerType.STREAMABLE_HTTP:
                    async with connection.get_client() as (
                        read_stream,
                        write_stream,
                        _,
                    ):
                        async with ClientSession(read_stream, write_stream) as session:
                            await session.initialize()
                            mcp_tool_result = await session.call_tool(
                                tool_name, arguments
                            )
                else:
                    async with connection.get_client() as (read_stream, write_stream):
                        async with ClientSession(read_stream, write_stream) as session:
                            await session.initialize()
                            mcp_tool_result = await session.call_tool(
                                tool_name, arguments
                            )
                tool_execute_result.content = str(mcp_tool_result.content)
                state_updates["status"] = Status.COMMON_TOOL_USE
            except Exception as e:
                root_error = e
                while root_error.__cause__:
                    root_error = root_error.__cause__
                logging.error(
                    f"call {server_name} tool {tool_name} error: {e}, root_error: {root_error}"
                )
                tool_execute_result.content = f"[Error] call {server_name} tool {tool_name} error: {e}, root_error: {root_error}"
                state_updates["status"] = Status.INVALID_TOOL_USE
            return tool_execute_result, state_updates

        case "generate_report":
            messages = state["messages"]

            # remove the system message
            messages = messages[1:]

            context = "\n\n".join([f"{msg.type}: {msg.content}" for msg in messages])
            info = f"""<context>
{context}
</context>"""

            report = await generate_report(info, await add_system_info(state["task"]))
            state_updates["result"] = report
            state_updates["status"] = Status.GENERATE_REPORT
            return tool_execute_result, state_updates
