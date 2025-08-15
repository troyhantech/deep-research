from enum import Enum
from typing import Any
from dataclasses import dataclass, field


@dataclass
class McpTool:
    name: str
    description: str | None = None
    input_schema: dict[str, Any] = field(default_factory=dict)


@dataclass
class McpResource:
    uri: str
    name: str
    description: str | None = None
    mime_type: str | None = None


@dataclass
class McpResourceTemplate:
    uri_template: str
    name: str
    description: str | None = None
    mime_type: str | None = None


@dataclass
class McpResourceResponse:
    contents: list[dict[str, str]]
    _meta: dict[str, Any] | None = None


@dataclass
class TextContent:
    text: str
    type: str = "text"


@dataclass
class ImageContent:
    data: str
    mime_type: str
    type: str = "image"


@dataclass
class ResourceContent:
    uri: str
    mime_type: str | None = None
    text: str | None = None
    blob: str | None = None
    type: str = "resource"

    @property
    def resource(self) -> dict[str, str | None]:
        return {
            "uri": self.uri,
            "mime_type": self.mime_type,
            "text": self.text,
            "blob": self.blob,
        }


@dataclass
class McpToolCallResponse:
    content: list[TextContent | ImageContent | ResourceContent]
    _meta: dict[str, Any] | None = None
    is_error: bool | None = None


@dataclass
class StdioConfig:
    command: str
    args: list[str]
    env: dict[str, str]


@dataclass
class SSEConfig:
    url: str


@dataclass
class StreamableHTTPConfig:
    url: str


class McpServerType(Enum):
    STDIO = "stdio"
    SSE = "sse"
    STREAMABLE_HTTP = "streamable_http"


@dataclass
class McpServerConfig:
    type: McpServerType
    config: StdioConfig | SSEConfig | StreamableHTTPConfig


class McpServerStatus(Enum):
    CONNECTED = "connected"
    CONNECTING = "connecting"
    DISCONNECTED = "disconnected"


@dataclass
class McpServer:
    name: str
    config: McpServerConfig
    status: McpServerStatus
    error: str | None = None
    tools: list[McpTool] | None = None
    resources: list[McpResource] | None = None
    resource_templates: list[McpResourceTemplate] | None = None
