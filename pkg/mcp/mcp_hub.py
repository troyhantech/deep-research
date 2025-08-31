import logging
from dataclasses import dataclass

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client

from pkg.mcp.types import (
    McpServer,
    McpServerConfig,
    McpServerStatus,
    McpServerType,
    McpTool,
    SSEConfig,
    StdioConfig,
    StreamableHTTPConfig,
)


@dataclass
class McpConnection:
    server: McpServer

    def get_client(self):
        client = None
        config = self.server.config
        if config.type == McpServerType.SSE:
            client = sse_client(config.config.url)

        elif config.type == McpServerType.STREAMABLE_HTTP:
            client = streamablehttp_client(config.config.url)

        elif config.type == McpServerType.STDIO:
            server_parameters = StdioServerParameters(
                command=config.config.command,
                args=config.config.args,
                env=config.config.env,
            )
            client = stdio_client(server_parameters)

        else:
            raise ValueError(f"invalid server type: {config.type}")
        return client


class McpHub:
    def __init__(self):
        self.connections: dict[str, McpConnection] = {}
        self.initialized = False

    async def init(self, mcp_server_configs: dict[str, McpServerConfig]):
        self.mcp_server_configs = mcp_server_configs
        if self.mcp_server_configs:
            await self._initialize_server_connections(self.mcp_server_configs)
        self.initialized = True
        logging.info("MCP servers initialized successfully!")

    async def _initialize_server_connections(
        self, server_config: dict[str, McpServerConfig]
    ):
        for name, config in server_config.items():
            try:
                logging.info(f"Connecting MCP server {name}...")
                await self._connect_to_server(name, config)
            except Exception as e:
                raise Exception(f"Failed to connect to MCP server {name}: {e}")
            logging.info(f"Connected to MCP server {name} successfully!")

    async def _connect_to_server(self, name: str, config: McpServerConfig):
        try:
            self.connections[name] = McpConnection(
                server=McpServer(
                    name=name,
                    status=McpServerStatus.CONNECTED,
                    config=config,
                ),
            )

            self.connections[name].server.tools = await self.list_tools(name)
        except Exception as e:
            connection = self.connections[name]
            if connection:
                connection.server.status = McpServerStatus.DISCONNECTED
                connection.server.error = str(e)
            raise e

    async def list_tools(self, server_name) -> list[McpTool]:
        try:
            server = self.connections[server_name]
            client = server.get_client()

            if (
                self.mcp_server_configs[server_name].type
                == McpServerType.STREAMABLE_HTTP
            ):
                async with client as (read_stream, write_stream, _):
                    async with ClientSession(read_stream, write_stream) as session:
                        await session.initialize()
                        tools_result = await session.list_tools()
            else:
                async with client as (read_stream, write_stream):
                    async with ClientSession(read_stream, write_stream) as session:
                        await session.initialize()
                        tools_result = await session.list_tools()
            tools = [
                McpTool(
                    name=tool.name,
                    description=tool.description,
                    input_schema=tool.inputSchema,
                )
                for tool in tools_result.tools
            ]

            return tools
        except Exception as e:
            raise Exception(f"fetch tools list for {server_name} failed: {e}")

    async def get_servers(self) -> list[McpServer]:
        if len(self.mcp_server_configs) == 0:
            return []
        if not self.initialized:
            raise Exception("MCP servers not initialized")
        return [connection.server for connection in self.connections.values()]


def convert_to_mcp_server_configs(
    mcp_servers_config: dict[str, dict],
) -> dict[str, McpServerConfig]:
    mcp_server_configs = {}
    _config = {}
    server_type = None
    for name, config in mcp_servers_config.items():
        if not config.get("enabled", False):
            continue

        match config.get("type", ""):
            case McpServerType.STDIO.value:
                _config = StdioConfig(
                    command=config.get("command", ""),
                    args=config.get("args", []),
                    env=config.get("env", {}),
                )
                server_type = McpServerType.STDIO
            case McpServerType.SSE.value:
                _config = SSEConfig(
                    url=config.get("url", ""),
                )
                server_type = McpServerType.SSE
            case McpServerType.STREAMABLE_HTTP.value:
                _config = StreamableHTTPConfig(
                    url=config.get("url", ""),
                )
                server_type = McpServerType.STREAMABLE_HTTP
            case _:
                raise ValueError(f"invalid server type: {config['type']}")

        mcp_server_configs[name] = McpServerConfig(
            type=server_type,
            config=_config,
        )
    return mcp_server_configs


mcp_hub = McpHub()
