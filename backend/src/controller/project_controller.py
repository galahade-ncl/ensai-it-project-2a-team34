from fastapi import APIRouter, Depends, HTTPException

from schema.audit_model import AuditReadModel
from schema.project_model import ProjectCreateModel, ProjectReadModel, ProjectResponseModel
from service.project_service import ProjectService
from utils.log_utils import get_logger
from utils.security import encode_secret_key, verify_token

router = APIRouter()

logger = get_logger(__name__)


def get_project_service():
    """
    Dependency injection provider for ProjectService.

    Returns
    -------
    ProjectService
        Instance of the project service.
    """
    return ProjectService()


# projects/ -> pas utile, on a déjà le chemin project/
@router.get("/{id_project}", response_model=ProjectReadModel, tags=["Projects"])
async def project_by_id(
    id_project: int, user=Depends(verify_token), project_service=Depends(get_project_service)
):
    """
    Find a project by its unique ID.

    Parameters
    ----------
    id_project : int
        Unique identifier of the project.
    user : User
        Authenticated user (injected by ``verify_token``).
    project_service : ProjectService
        Service used to interact with project data.

    Returns
    -------
    ProjectReadModel
        The project data if found.

    Raises
    ------
    HTTPException
        404 error if the project is not found or not owned by the user.
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
    """
    Create a new project.

    Parameters
    ----------
    p : ProjectCreateModel
        Project data to create.
    user : User
        Authenticated user (injected by ``verify_token``).
    project_service : ProjectService
        Service used to interact with project data.

    Returns
    -------
    ProjectResponseModel
        The newly created project, with its secret HMAC key encoded
        in Base64.

    Raises
    ------
    HTTPException
        500 error if the creation process fails.
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
    """
    Delete a project from the system.

    Parameters
    ----------
    id_project : int
        Unique identifier of the project.
    user : User
        Authenticated user (injected by ``verify_token``).
    project_service : ProjectService
        Service used to interact with project data.

    Returns
    -------
    str
        Confirmation message indicating the project was deleted.

    Raises
    ------
    HTTPException
        404 error if the project is not found or not owned by the user.
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
    """
    Update an existing project's information.

    Parameters
    ----------
    id_project : int
        Unique identifier of the project.
    p : ProjectCreateModel
        New data for the project.
    user : User
        Authenticated user (injected by ``verify_token``).
    project_service : ProjectService
        Service used to interact with project data.

    Returns
    -------
    ProjectReadModel
        The updated project data.

    Raises
    ------
    HTTPException
        404 error if the project is not found or not owned by the user.
    HTTPException
        500 error if the update process fails.
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
    """
    Generate a new secret key for a project.

    The old key stops working.

    Parameters
    ----------
    id_project : int
        Unique identifier of the project.
    user : User
        Authenticated user (injected by ``verify_token``).
    project_service : ProjectService
        Service used to interact with project data.

    Returns
    -------
    dict
        Dictionary containing ``id_project``, ``name_project`` and the
        new ``secretHMACkey``.

    Raises
    ------
    HTTPException
        404 error if the project is not found or not owned by the user.
    HTTPException
        500 error if the key could not be regenerated.
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
    """
    Retrieve the audits of a project.

    Parameters
    ----------
    id_project : int
        Unique identifier of the project.
    user : User
        Authenticated user (injected by ``verify_token``).
    project_service : ProjectService
        Service used to interact with project data.

    Returns
    -------
    list of AuditReadModel
        Audits of the project.

    Raises
    ------
    HTTPException
        404 error if the project is not found or not owned by the user.
    """
    project = project_service.find_by_id_and_user(id_project, user.id_user)
    if not project:
        raise HTTPException(
            status_code=404, detail="Project not found or you do not have access to it."
        )
    return project_service.list_all_audit(id_project)
