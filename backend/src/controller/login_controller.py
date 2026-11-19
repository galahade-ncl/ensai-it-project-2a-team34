from fastapi import APIRouter, Depends, HTTPException

from schema.user_model import UserLoginModel
from service.user_service import UserService
from utils.log_utils import get_logger

router = APIRouter()

logger = get_logger(__name__)


def get_user_service():
    """
    Dependency injection provider for UserService.

    Returns
    -------
    UserService
        Instance of the user service.
    """
    return UserService()


@router.post("/", tags=["Login"])
def login(credentials: UserLoginModel, service=Depends(get_user_service)):
    """
    Authenticate a user.

    Parameters
    ----------
    credentials : UserLoginModel
        Username and password of the user.
    service : UserService
        Service used to interact with user data.

    Returns
    -------
    dict
        Dictionary containing ``id_user``, ``username`` and
        ``access_token``.

    Raises
    ------
    HTTPException
        401 error if the credentials are invalid or the user does not exist.
    """
    logger.info("Login")
    user = service.login(credentials.username, credentials.password)
    if user:
        return {
            "id_user": user.id_user,
            "username": user.username,
            "access_token": user.access_token,
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")
