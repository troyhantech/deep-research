import json

from pkg.mcp.mcp_hub import mcp_hub
from pkg.mcp.types import McpServerStatus

from string import Template


async def get_mcp_server_description(contain_input_schema: bool = False) -> str:
    servers = await mcp_hub.get_servers()

    if len(servers) == 0:
        return "No MCP servers are connected, use your existing knowledge to answer."

    description = ""
    for server in servers:
        if server.status != McpServerStatus.CONNECTED:
            continue

        tools_description = ""
        for tool in server.tools:
            schema_str = ""
            if contain_input_schema and tool.input_schema:
                schema_str = f"""Input Schema:
{json.dumps(tool.input_schema, indent=2, ensure_ascii=False)}
"""
            tools_description += f"""
- {tool.name}: {tool.description}
{schema_str}"""

        description += f"""
### {server.name}
{tools_description}
"""

    return description


MCP_SERVERS_PROMPT_TEMPLATE = Template(
    """
# MCP SERVERS

The Model Context Protocol (MCP) enables communication between the system and locally running MCP servers that provide additional tools and resources to extend your capabilities.

You can use the MCP servers' tools via the `call_mcp_tool` tool.

##  MCP Servers And Tools

$mcp_server_description
"""
)


async def get_mcp_prompt() -> str:
    mcp_server_description = await get_mcp_server_description(True)

    if mcp_server_description == "":
        return ""

    return MCP_SERVERS_PROMPT_TEMPLATE.substitute(
        {"mcp_server_description": mcp_server_description}
    )
