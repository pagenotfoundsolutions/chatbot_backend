from app.modules.tools.application.queries.get_all_tools.get_all_tools_handler import GetAllToolsHandler
from app.modules.tools.application.ports.input.get_all_tools_use_case import GetAllToolsUseCase


def get_all_tools_use_case() -> GetAllToolsUseCase:
    """Dependency provider for GetAllToolsUseCase."""
    return GetAllToolsHandler()
