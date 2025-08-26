from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter()


@router.get("/web")
async def read_web():
    return FileResponse("deep_research_interface.html")
