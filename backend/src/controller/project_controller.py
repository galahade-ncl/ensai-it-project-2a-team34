from fastapi import APIRouter, Depends, HTTPException

from schema.project_model import ProjectModel
from service.project_service import ProjectService
from utils.log_utils import get_logger

router = APIRouter()

logger = get_logger(__name__)


def get_project_service():
    """Dependency Injection provider for FileService."""
    return ProjectService()


@router.get("/{id_project}", response_model=ProjectModel, tags=["Project"])
async def project_by_id(id_project: int, project_service=Depends(get_project_service)):
    """Find a project by its unique ID.
    Args:
        id_project (int)
        project_service (ProjectService): The service used to interact with project data
    Returns:
        ProjectModel: The project data if found
    Raises:
        HTTPException: 404 error if the project is not found
    """
    logger.info("Find a project by id")
    project = project_service.find_by_id(id_project)
    if not project:
        raise HTTPException(status_code=404, detail="Project (id={id_project}) not found.")
    return project


@router.get("/", response_model=list[ProjectModel], tags=["Projects"])
async def project_by_user(id_user: int, project_service=Depends(get_project_service)):
    """
    Retrieve projects filtered by user ID.
    """

    return project_service.list_all_project(id_user)
