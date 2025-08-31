from config import get_config
import logging

from agents.deep_research import deep_research as _deep_research

from fastmcp import FastMCP

mcp = FastMCP("Deep-Research MCP")


@mcp.tool
async def deep_research(task: str) -> str:
    """Deep research the input topic task and generate a report"""
    try:
        logging.info(f"deep research task: {task}")

        agents_config = get_config().get("agents", {})
        logging.info(f"deep research agents config: {agents_config}")

        result = await _deep_research(task, agents_config)
    except Exception as e:
        logging.error(f"failed to deep research: {e}", exc_info=True)
        return "Internal Error"
    return result
