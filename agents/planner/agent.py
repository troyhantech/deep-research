import logging
from agents.planner.prompt import (
    get_system_prompt,
    tool_names,
    tool_params_names,
)
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import START, END, StateGraph
from langchain_core.messages.utils import convert_to_openai_messages
from agents.planner.tool_executor import execute_tool
from pkg.openai_client import async_openai_sdk_client
from config import CONFIG
from agents.tool_content_parser import parse_xml_tool_content
from agents.response import Response
from agents.planner.schema import State, Status
from datetime import datetime
from agents.reporter.agent import generate_report


async def add_system_info(content: str) -> str:
    current_time = datetime.now().astimezone().isoformat()

    return f"""<task>
{content}
</task>

<system_info>
1. current time: {current_time}
</system_info>"""


async def reasoning_node(state: State) -> State:
    messages = state.get("messages", [])
    task = state.get("task", "")

    # add system prompt
    system_prompt = await get_system_prompt()
    if not messages:
        messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=await add_system_info(task)))
    else:
        messages[0].content = system_prompt

    # call reasoning model
    try:

        response = await async_openai_sdk_client.chat.completions.create(
            model=CONFIG["agents"]["planner"]["model"],
            messages=convert_to_openai_messages(messages),
            max_tokens=CONFIG["agents"]["planner"]["max_tokens"],
        )
    except Exception as e:
        logging.error(f"failed to call reasoning model: {e}")
        raise e

    messages.append(
        AIMessage(
            content=response.choices[0].message.content,
        )
    )

    return {
        "messages": messages,
    }


async def action_node(state: State) -> State:
    messages = state["messages"]
    reasoning_result = messages[-1].content

    # get tool use block
    parsed_result = parse_xml_tool_content(
        reasoning_result, tool_names=tool_names, tool_params_names=tool_params_names
    )

    tool_use_blocks = [item for item in parsed_result if item["type"] == "tool_use"]

    # check whether use tool
    if len(tool_use_blocks) == 0:
        logging.warning("no tool use")
        messages.append(HumanMessage(content=Response.noToolUse))
        return {
            "status": Status.INVALID_TOOL_USE,
            "messages": messages,
        }

    # only execute one tool
    tool_use = tool_use_blocks[0]

    if tool_use["partial"]:
        logging.warning("partial tool use")
        messages.append(HumanMessage(content=Response.partialToolUse))
        return {
            "status": Status.INVALID_TOOL_USE,
            "messages": messages,
        }

    tool_execute_result, state_updates = await execute_tool(state, tool_use)

    action_result = tool_execute_result.content

    messages.append(
        HumanMessage(
            content=action_result,
        )
    )

    # call model to generate report directly
    remaining_reasoning_times = state["remaining_reasoning_times"] - 1
    if (
        remaining_reasoning_times <= 1
        and state_updates["status"] != Status.GENERATE_REPORT
    ):
        # remove system prompt
        messages = messages[1:]

        context = "\n\n".join([f"{msg.type}: {msg.content}" for msg in messages])
        info = f"""<context>
{context}
</context>
"""

        report = await generate_report(info, await add_system_info(state["task"]))
        return {"result": report, "status": Status.GENERATE_REPORT}
    return {
        "messages": messages,
        **state_updates,
        "remaining_reasoning_times": state["remaining_reasoning_times"] - 1,
    }


async def action_result_condition(state: State) -> str:
    match state["status"]:
        case Status.GENERATE_REPORT:
            return "break_reasoning"
        case _:
            return "continue_reasoning"


agent = None


def create_agent():
    global agent
    if agent:
        return agent
    workflow = StateGraph(State)
    workflow.add_node("reasoning_node", reasoning_node)
    workflow.add_node("action_node", action_node)

    workflow.add_edge(START, "reasoning_node")
    workflow.add_edge("reasoning_node", "action_node")

    workflow.add_conditional_edges(
        "action_node",
        action_result_condition,
        {
            "break_reasoning": END,
            "continue_reasoning": "reasoning_node",
        },
    )

    agent = workflow.compile()
    return agent
