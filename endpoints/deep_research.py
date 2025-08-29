from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from agents.deep_research import deep_research as _deep_research
from config import CONFIG
from pkg.utils import deep_update

router = APIRouter()


class DeepResearchRequest(BaseModel):
    task: str
    config: Optional[dict] = None


@router.post("/deep-research", operation_id="deep_research")
async def deep_research(request: DeepResearchRequest):
    """Deep research the input topic task and generate a report"""
    try:
        logging.info(f"deep research request: {request}")

        agents_config = CONFIG.get("agents", {})
        if request.config:
            deep_update(agents_config, request.config)

        logging.info(f"deep research agents config: {agents_config}")

        result = await _deep_research(request.task, agents_config)
    except Exception as e:
        logging.error(f"failed to deep research: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"message": "Internal Error"})
    return {"result": result}
