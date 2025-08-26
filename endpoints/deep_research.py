from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from agents.deep_research import deep_research as _deep_research


router = APIRouter()


class DeepResearchRequest(BaseModel):
    task: str


@router.post("/deep-research", operation_id="deep_research")
async def deep_research(request: DeepResearchRequest):
    """Deep research the input topic task and generate a report"""
    try:
        result = await _deep_research(request.task)
    except Exception as e:
        logging.error(f"failed to deep research: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"message": "Internal Error"})
    return {"result": result}
