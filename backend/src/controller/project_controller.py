from fastapi import APIRouter, Depends, HTTPException

from schema.project_model import ProjectCreateModel, ProjectReadModel, ProjectResponseModel
from service.project_service import ProjectService
from utils.log_utils import get_logger

router = APIRouter()

logger = get_logger(__name__)


def get_project_service():
    """Dependency Injection provider for FileService."""
    return ProjectService()


@router.get("projects/{id_project}", response_model=ProjectReadModel, tags=["Projects"])
async def project_by_id(id_project: int, project_service=Depends(get_project_service)):
    """Find a project by its unique ID.
    Args:
        id_project (int)
        project_service (ProjectService): The service used to interact with project data
    Returns:
        ProjectRead: The project data if found
    Raises:
        HTTPException: 404 error if the project is not found
    """
    logger.info("Find a project by id")
    project = project_service.find_by_id(id_project)
    if not project:
        raise HTTPException(status_code=404, detail="Project (id={id_project}) not found.")
    return project



@router.get("users/{id_user}/projects", response_model=list[ProjectReadModel], tags=["Projects"])
async def project_by_user(id_user: int, project_service=Depends(get_project_service)):
    """
    Retrieve projects filtered by user ID.
    """

    return project_service.list_all_projects(id_user)



@router.post("/projects", response_model=ProjectResponseModel, tags=["Projects"])
async def create_project(p: ProjectCreateModel, project_service=Depends(get_project_service)):
    """Create a new project.
    Args:
        p (ProjectCreateModel): The project data to create.
        project_service (ProjectService): The service used to interact with project data.
    Returns:
        ProjectResponseModel: The newly created project data.
    Raises:
        HTTPException: 500 error if the creation process fails.
    """
    logger.info("Create a project")

    project = project_service.upload(p.name, p.user)
    if not project:
        raise HTTPException(status_code=500, detail="Error while creating project.")

    return project


@router.delete("/{id_project}", tags=["Projects"])
async def delete_project(id_project: int, project_service=Depends(get_project_service)):
    """Delete a project from the system.
    Args:
        id_project (int)
        project_service (ProjectService): The service used to interact with project data.
    Returns:
        str: A confirmation message indicating the project was deleted.
    Raises:
        HTTPException: 404 error if the project is not found.
    """
    logger.info("Delete a project")
    project = project_service.find_by_id(id_project)
    if not project:
        raise HTTPException(status_code=404, detail="Project (id={id_project}) not found.")

    project_service.delete(project)
    return f"Project {project.name_project} deleted"


@router.put("/{id_project}", response_model=ProjectReadModel, tags=["Projects"])
async def update_project(id_project: int, p: ProjectCreateModel, project_service=Depends(get_project_service)):
    """Update an existing project's information.
    Args:
        id_project (int)
        p (ProjectCreateModel): The new data for the project.
        project_service (ProjectService): The service used to interact with project data.
    Returns:
        str: A confirmation message indicating the project was updated.
    Raises:
        HTTPException: 404 error if the project is not found.
        HTTPException: 500 error if the update process fails.
    """
    logger.info("Update a project")
    project = project_service.find_by_id(id_project)
    if not project:
        raise HTTPException(status_code=404, detail="Project (id={id_project}) not found.")

    project.name_project = p.name_project
    project.user = p.user

    project = project_service.update(project)
    if not project:
        raise HTTPException(status_code=500, detail="Error while updating project.")

    return project
