from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from agents.worker.prompt_blocks.mcp_servers import get_mcp_server_description
from endpoints.http_server import router as http_router
from pkg.mcp.mcp_hub import mcp_hub
from config import CONFIG
from fastapi_mcp import FastApiMCP

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("connecting mcp servers...")
    try:
        await mcp_hub.initialize()
    except Exception as e:
        raise Exception(f"failed to connect mcp servers: {e}")

    mcp_server_description = await get_mcp_server_description(True)
    print(mcp_server_description)

    logging.info("initializing successfully")
    yield


# http server
app = FastAPI(lifespan=lifespan)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

app.include_router(http_router)


@app.get("/web")
async def read_web():
    return FileResponse("deep_research_interface.html")


# mcp server
mcp = FastApiMCP(app, name="DeepResearch")
mcp.mount()


if __name__ == "__main__":
    import uvicorn
    from uvicorn.config import LOGGING_CONFIG

    LOGGING_CONFIG["formatters"]["default"][
        "fmt"
    ] = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=LOGGING_CONFIG)
