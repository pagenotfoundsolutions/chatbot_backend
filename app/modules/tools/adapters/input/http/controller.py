from fastapi import APIRouter, Depends

from app.modules.tools.application.ports.input.get_all_tools_use_case import GetAllToolsUseCase
from app.modules.tools.adapters.input.http.dependencies import get_all_tools_use_case


router = APIRouter(prefix="/tools", tags=["Tools"])

@router.get("")
def list_tools(use_case: GetAllToolsUseCase = Depends(get_all_tools_use_case)) -> list[dict]:
    """Returns a list of all active tools available to the AI agent."""
    tools = use_case.execute()
    return [
        {
            "name": t.name,
            "description": t.description
        }
        for t in tools
    ]
