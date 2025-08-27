from agents.worker.prompt_blocks.mcp_servers import get_mcp_server_description


async def get_worker_agent_capabilities() -> str:
    mcp_server_description = await get_mcp_server_description()
    return f"""
# Worker Agent Capabilities

Worker can use the below server and tools to complete the subtask:

{mcp_server_description}
"""
