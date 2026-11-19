from fastapi import APIRouter, Depends, HTTPException

from schema.audit_model import AuditReadModel
from schema.project_model import ProjectCreateModel, ProjectReadModel, ProjectResponseModel
from service.project_service import ProjectService
from utils.log_utils import get_logger
from utils.security import encode_secret_key, verify_token

router = APIRouter()

logger = get_logger(__name__)


def get_project_service():
    """Dependency Injection provider for FileService."""
    return ProjectService()


# projects/ -> pas utile, on a déjà le chemin project/
@router.get("/{id_project}", response_model=ProjectReadModel, tags=["Projects"])
async def project_by_id(
    id_project: int, user=Depends(verify_token), project_service=Depends(get_project_service)
):
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
    project = project_service.find_by_id_and_user(id_project, user.id_user)
    if not project:
        raise HTTPException(
            status_code=404, detail="Project not found or you do not have access to it."
        )
    return project


@router.post("/", response_model=ProjectResponseModel, tags=["Projects"])
async def create_project(
    p: ProjectCreateModel, user=Depends(verify_token), project_service=Depends(get_project_service)
):
    """Create a new project.
    Args:
        p (ProjectCreateModel): The project data to create.
        user (user): authentified User
        project_service (ProjectService): The service used to interact with project data.
    Returns:
        ProjectResponseModel: The newly created project data.
    Raises:
        HTTPException: 500 error if the creation process fails.
    """
    logger.info("Create a project")

    project = project_service.upload(p.name_project, user)
    if not project:
        raise HTTPException(status_code=500, detail="Error while creating project.")

    # Application du ProjectResponseModel
    response_project = ProjectResponseModel(
        id_project=project.id_project,
        name_project=project.name_project,
        secretHMACkey=encode_secret_key(project.secretHMACkey),
    )
    return response_project


@router.delete("/{id_project}", tags=["Projects"])
async def delete_project(
    id_project: int, user=Depends(verify_token), project_service=Depends(get_project_service)
):
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
    project = project_service.find_by_id_and_user(id_project, user.id_user)
    if not project:
        raise HTTPException(
            status_code=404, detail="Project not found or you do not have access to it."
        )

    project_service.delete(project)
    return f"Project {project.name_project} deleted"


@router.put("/{id_project}", response_model=ProjectReadModel, tags=["Projects"])
async def update_project(
    id_project: int,
    p: ProjectCreateModel,
    user=Depends(verify_token),
    project_service=Depends(get_project_service),
):
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
    project = project_service.find_by_id_and_user(id_project, user.id_user)
    if not project:
        raise HTTPException(
            status_code=404, detail="Project not found or you do not have access to it."
        )

    project.name_project = p.name_project

    project = project_service.update(project)
    if not project:
        raise HTTPException(status_code=500, detail="Error while updating project.")

    return project


@router.post("/{id_project}/secret-key", tags=["Projects"])
async def regenerate_secret_key(
    id_project: int,
    user=Depends(verify_token),
    project_service=Depends(get_project_service),
):
    """Regenerates the secret HMAC key of a project.
    Args:
        id_project: ID of the project whose secret key must be regenerated.
        user: Authenticated user obtained through token verification.
        project_service: Project service used to retrieve the project and regenerate its secret key.
    Returns:
        dict: containing:
            - id_project: Project identifier.
            - name_project: Project name.
            - secretHMACkey: Newly generated secret HMAC key.
    Raises:
        HTTPException:
            401 error if the authentication token is invalid or missing.
            404 error if the project does not exist or the user does not have access to it.
            500 error if the secret key could not be regenerated.
    """
    project = project_service.find_by_id_and_user(id_project=id_project, id_user=user.id_user)
    if not project:
        raise HTTPException(
            status_code=404, detail="Project not found or you do not have access to it."
        )

    new_key = project_service.regenerate_secret_key(project)
    if not new_key:
        raise HTTPException(status_code=500, detail="Could not regenerate the secret key.")

    return {
        "id_project": project.id_project,
        "name_project": project.name_project,
        "secretHMACkey": new_key,
    }


@router.get("/{id_project}/audit", response_model=list[AuditReadModel], tags=["Projects"])
async def audit_by_project(
    id_project: int, user=Depends(verify_token), project_service=Depends(get_project_service)
):
    """Retrieves all audits associated with a project.
    Args:
        id_project: ID of the project whose audits must be retrieved.
        user: Authenticated user obtained through token verification.
        project_service: Project service used to retrieve the project and its audits.
    Returns:
        list[AuditReadModel]: List of audits associated with the specified project.
    Raises:
        HTTPException:
            401 error if the authentication token is invalid or missing.
            404 error if the project does not exist or the user does not have access to it.
    """
    project = project_service.find_by_id_and_user(id_project, user.id_user)
    if not project:
        raise HTTPException(
            status_code=404, detail="Project not found or you do not have access to it."
        )
    return project_service.list_all_audit(id_project)
