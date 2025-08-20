# DeepResearch

<div align="center">

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10+-green.svg)](https://python.org)
![Fast](https://img.shields.io/badge/fast-HTTP_&_MCP-g.svg)

[中文](README.md) | English

</div>

A simple, direct, and highly scalable deep research tool based on multi-agent architecture, supporting arbitrary LLM and MCP tool integration.

## ✨ Features

- 🔌 **OpenAI API Compatible**: Supports any LLM compatible with OpenAI API, no function calling capability required.
- 🛠️ **Universal MCP Extension**: Supports integration of arbitrary MCP tools (stdio, streamable or sse) to extend Agent capabilities.
- 🌐 **Simple and Intuitive**: Exposes both HTTP and MCP interfaces with clean APIs for easy integration.
- ⚡ **High-Performance Async**: Built on FastAPI, supports high-concurrency request processing.

## How It Works

```mermaid
flowchart TD
    Task(["Task"]) --> AgentSystem

    subgraph AgentSystem["Loop"]
        Planner["📋 Planner Agent"]
        Worker1["🔧 Worker  Agent 1"]
        Worker2["🔧 Worker  Agent 2"]
        Worker3["🔧 Worker  Agent N"]

        Planner --> Worker1
        Planner --> Worker2
        Planner --> Worker3

        Worker1 --> Planner
        Worker2 --> Planner
        Worker3 --> Planner
    end

    AgentSystem --> Report(["Report"])
```

The general workflow is as follows:

1. The user submits a research task to the system.
2. The planner analyzes the task and dispatches initial-stage subtasks to workers(no more than 10 subtasks).
3. Workers execute the subtasks in parallel, and return the subtask reports.
4. Subtasks reports are aggregated and passed to the planner.
5. The planner analyzes the context and the subtask results to determine next action.
6. This process repeats until the research goal is met.
7. The system delivers the final report to the user.

## 🚀 Quick Start

### System Requirements

- Python 3.10+

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/deep-research.git
cd deep-research
```

### 2. Install Dependencies

```bash
pip install uv
uv pip install -r requirements.txt

# or

pip install -r requirements.txt
```

### 3. Configuration

#### 3.1 Environment Variables

Copy the template file:

```bash
cp .env.example .env
```

Edit the `.env` file and configure your API keys:

```env
OPENAI_API_KEY="your-openai-api-key"
OPENAI_BASE_URL="https://api.openai.com/v1/"

# Optional: LangSmith tracing
LANGSMITH_TRACING="true"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="your-langsmith-api-key"
LANGSMITH_PROJECT="your-langsmith-project"
```

#### 3.2 Application Configuration

Copy the template file:

```bash
cp config.toml.example config.toml
```

Edit `config.toml` to configure agents and MCP services:

```toml
[agents]
[agents.planner]
model = "gpt-4o"
max_reasoning_times = 5
max_tokens = 4096

[agents.reporter]
model = "gpt-4o"
max_tokens = 4096

[agents.worker]
model = "gpt-4o"
max_tokens = 4096
max_reasoning_times = 5

# Support three standard MCP transport as worker tools: streamable_http、stdio or sse.
[mcp_servers]

# use streamable_http tavily
[mcp_servers.tavily_streamable_http]
enabled = true
type = "streamable_http"
url = "https://mcp.tavily.com/mcp/?tavilyApiKey=your-tavily-api-key"

# or use stdio
[mcp_servers.tavily_stdio]
enabled = false
type = "stdio"
command = "npx"
args = ["-y", "mcp-remote", "https://mcp.tavily.com/mcp/?tavilyApiKey=your-tavily-api-key"]

# add any other sse server
[mcp_servers.sse_server_example]
enabled = false
type = "sse"
url = "sse_server_url"
```

### 4. Start the Service

```bash
python main.py
```

Exposed endpoints:

- HTTP Service: `http://localhost:8000`
- MCP Service: `http://localhost:8000/mcp`

## 📖 Usage Guide

### HTTP Interface

Request this interface by HTTP POST, send your research task, wait for a while, and get a comprehensive report.

**POST** `/deep-research`

**Request Body:**

```json
{
  "task": "Analyze Bitcoin price trends for the next month."
}
```

**Response Body:**

```json
{
  "result": "# Bitcoin Price Trends Analysis for the Next Month\n\n## Introduction\n\nThis report provides an analysis of Bitcoin price trends for the next month..."
}
```

**Quick Start Examples:**

```bash
curl -X POST "http://localhost:8000/deep-research" \
     -H "Content-Type: application/json" \
     -d '{"task": "Analyze Bitcoin price trends for the next month."}'
```

> **Usage Tips**
>
> Task should be clear and specific, for example:
>
> ```txt
> Research the economic impact of semaglutide on global healthcare systems.
> Do:
> - Include specific figures, trends, statistics, and measurable outcomes.
> - Prioritize reliable, up-to-date sources: peer-reviewed research, health
>   organizations (e.g., WHO, CDC), regulatory agencies, or pharmaceutical
>   earnings reports.
> - Include inline citations and return all source metadata.
>
> Be analytical, avoid generalities, and ensure that each section supports
> data-backed reasoning that could inform healthcare policy or financial modeling.
> ```

### MCP Interface

The service also exposes an MCP interface, allowing this service to be used as an MCP service by any MCP client.

Configure in MCP client:

```json
{
  "mcpServers": {
    "deep-research": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## ❓ Frequently Asked Questions (FAQ)

### Q: Which LLM models are supported?

A: Supports any model compatible with OpenAI API, including OpenAI GPT series, OpenRouter, etc.

### Q: Must I use models with Function Call capabilities?

A: No, this project does not depend on the model's Function Call functionality. Any large language model will work.

### Q: Is prompt caching supported?

A: No, prompt caching is not supported. However, most of the models support automatic caching mechanism, and there are enough models support it.

### Q: How to add custom MCP tools?

A: Add your MCP service configuration in the `[mcp_servers]` section of the `config.toml` file. For example: integrate custom knowledge base search MCP services.

### Q: If I don't add any MCP tools, will there be any impact?

A: No, there will be no impact. The system will still work, but agent won't be able to use MCP tools, and answer using their existing knowledge.

### Q: Only Python 3.10+ is supported?

A: No, the author only tests with Python 3.10+, but it should work with 3.8+ as well.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome all forms of contributions! Whether it's reporting bugs, suggesting new features, or submitting code improvements.

## 🐛 Issue Reporting

If you find bugs or have feature suggestions, please submit them on the [Issues](https://github.com/troyhantech/deep-research/issues) page.

## ⭐ Star History

If this project helps you, please give us a ⭐!

[![Star History Chart](https://api.star-history.com/svg?repos=troyhantech/deep-research&type=Date)](https://star-history.com/#troyhantech/deep-research&Date)

---

<div align="center">
  <p>Made with ❤️ by the troyhantech</p>
  <p>If you like this project, please consider giving it a ⭐</p>
</div>
