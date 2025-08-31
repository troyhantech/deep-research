from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from agents.deep_research import deep_research as _deep_research
from config import get_config
from pkg.utils import deep_update
from pydantic import Field

router = APIRouter()


class DeepResearchRequest(BaseModel):
    task: str = Field(description="The topic task to deep research")
    config: Optional[dict] = Field(
        None, description="The config to override the default config"
    )


class DeepResearchResponse(BaseModel):
    result: str = Field(description="The deep research result")


@router.post("/deep-research", operation_id="deep_research")
async def deep_research(request: DeepResearchRequest) -> DeepResearchResponse:
    """Deep research the input topic task and generate a report"""
    try:
        logging.info(f"deep research request: {request}")

        agents_config = get_config().get("agents", {})
        if request.config:
            deep_update(agents_config, request.config)

        logging.info(f"deep research agents config: {agents_config}")

        result = await _deep_research(request.task, agents_config)
    except Exception as e:
        logging.error(f"failed to deep research: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"message": "Internal Error"})
    return DeepResearchResponse(result=result)
