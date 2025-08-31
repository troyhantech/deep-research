import logging
import argparse
import asyncio
import argparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.worker.prompt_blocks.mcp_servers import get_mcp_server_description
from endpoints.api.deep_research import router as deep_research_router
from endpoints.api.web import router as web_router
from pkg.mcp.mcp_hub import mcp_hub, convert_to_mcp_server_configs
from config import init_config
from endpoints.mcp.deep_research import mcp
from pkg.openai_client import init_openai_client

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def init(env_file: str, config_file: str):
    logging.info(f"init config...")
    config = init_config(env_file, config_file)

    init_openai_client()

    logging.info("connecting mcp servers...")
    try:
        await mcp_hub.init(convert_to_mcp_server_configs(config["mcp_servers"]))
    except Exception as e:
        raise Exception(f"failed to connect mcp servers: {e}")

    mcp_server_description = await get_mcp_server_description(True)
    logging.info(f"MCP SERVER DESCRIPTION:\n {mcp_server_description}")

    logging.info("initializing successfully")


def start_server(mode: str, host: str, port: int):
    match mode:
        case "mcp_stdio":
            mcp.run()
        case "mcp_streamable_http":
            mcp.run(transport="streamable-http", host=host, port=port)
        case "http_api":
            app = FastAPI(title="Deep-Research API")

            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

            app.include_router(deep_research_router)
            app.include_router(web_router)

            # run server
            import uvicorn
            from uvicorn.config import LOGGING_CONFIG

            LOGGING_CONFIG["formatters"]["default"][
                "fmt"
            ] = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            LOGGING_CONFIG["formatters"]["access"][
                "fmt"
            ] = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            uvicorn.run(app, host=host, port=port, log_config=LOGGING_CONFIG)
        case _:
            raise ValueError(f"invalid launch mode: {mode}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--env-file",
        default="./.env",
        help="path to .env file (e.g. /app/config/.env)",
    )
    parser.add_argument(
        "--config-file",
        default="./config.toml",
        help="path to config.toml (e.g. /app/config/config.toml)",
    )

    # transport argument
    parser.add_argument(
        "--mode",
        default="mcp_stdio",
        choices=["mcp_stdio", "mcp_streamable_http", "http_api"],
        help="Launch mode: mcp_stdio, mcp_streamable_http, or http_api",
    )
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    asyncio.run(init(args.env_file, args.config_file))

    start_server(args.mode, args.host, args.port)
