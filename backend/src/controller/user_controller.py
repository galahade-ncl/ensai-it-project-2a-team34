from fastapi import APIRouter, Depends, HTTPException

from schema.project_model import ProjectReadModel
from schema.user_model import UserModel, UserReadModel, UserResponseModel
from service.project_service import ProjectService
from service.user_service import UserService
from utils.log_utils import get_logger
from utils.security import verify_token

router = APIRouter()

logger = get_logger(__name__)


def get_user_service() -> UserService:
    """
    Dependency injection provider for UserService.

    Returns
    -------
    UserService
        Instance of the user service.
    """
    return UserService()


def get_project_service() -> ProjectService:
    """
    Dependency injection provider for ProjectService.

    Returns
    -------
    ProjectService
        Instance of the project service.
    """
    return ProjectService()


@router.post("/", response_model=UserReadModel, tags=["Users"])
async def create_user(u: UserModel, user_service=Depends(get_user_service)) -> UserReadModel:
    """
    Create a new user.

    Parameters
    ----------
    u : UserModel
        User data to create.
    user_service : UserService
        Service used to interact with user data.

    Returns
    -------
    UserReadModel
        The newly created user data.

    Raises
    ------
    HTTPException
        400 error if the username is already taken.
    HTTPException
        500 error if the creation process fails.
    """
    logger.info("Create a player")
    if user_service.username_already_used(u.username):
        raise HTTPException(status_code=400, detail="Username already used.")

    user = user_service.create(u.username, u.password, u.email)
    if not user:
        raise HTTPException(status_code=500, detail="Error while creating user.")

    return user


@router.put("/{id_user}", response_model=UserReadModel, tags=["Users"])
async def update_user(
    u: UserResponseModel, user=Depends(verify_token), user_service=Depends(get_user_service)
):
    """
    Update the information of the authenticated user.

    Parameters
    ----------
    u : UserResponseModel
        New data for the user.
    user : User
        Authenticated user (injected by ``verify_token``).
    user_service : UserService
        Service used to interact with user data.

    Returns
    -------
    UserReadModel
        The updated user data.

    Raises
    ------
    HTTPException
        400 error if the new username is already taken.
    HTTPException
        404 error if the user is not found.
    HTTPException
        500 error if the update process fails.
    """
    logger.info("Update a user")
    if not user:
        raise HTTPException(status_code=404, detail=f"User (id={user.id_user}) not found.")
    if user_service.username_already_used(u.username):
        raise HTTPException(status_code=400, detail="Username already used.")

    user.username = u.username
    user.password = u.password
    user.email = u.email

    user = user_service.update(user)
    if not user:
        raise HTTPException(status_code=500, detail="Error while updating player.")

    return user


@router.delete("/{id_user}", tags=["Users"])
async def delete_user(
    user=Depends(verify_token),
    user_service=Depends(get_user_service),
    project_service=Depends(get_project_service),
) -> str:
    """
    Delete the authenticated user and all their projects.

    Parameters
    ----------
    user : User
        Authenticated user (injected by ``verify_token``).
    user_service : UserService
        Service used to interact with user data.
    project_service : ProjectService
        Service used to delete the projects of the user.

    Returns
    -------
    str
        Confirmation message indicating the user was deleted.

    Raises
    ------
    HTTPException
        404 error if the user is not found.
    """
    logger.info("Delete a user")

    if not user:
        raise HTTPException(status_code=404, detail=f"User (id={user.id_user}) not found.")

    # Delete all project own by the user
    list_project = user_service.list_all_project(user.id_user)
    for project in list_project:
        project_service.delete(project)

    # Delete the user
    user_service.delete(user)
    return f"User {user.username} deleted"


@router.get("/{id_user}/project", response_model=list[ProjectReadModel], tags=["Users"])
async def project_by_user(
    user=Depends(verify_token), user_service=Depends(get_user_service)
) -> list[ProjectReadModel]:
    """
    Retrieve the projects of the authenticated user.

    Parameters
    ----------
    user : User
        Authenticated user (injected by ``verify_token``).
    user_service : UserService
        Service used to interact with user data.

    Returns
    -------
    list of ProjectReadModel
        Projects owned by the user.
    """
    id_user = user.id_user
    return user_service.list_all_project(id_user)
