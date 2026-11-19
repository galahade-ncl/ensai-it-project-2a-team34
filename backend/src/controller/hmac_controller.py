import base64

from fastapi import APIRouter

from utils.log_utils import get_logger
from utils.security import generate_signature

router = APIRouter()

logger = get_logger(__name__)


@router.post("/signature")
async def create_hmac_signature(secret, project_id, code, dependency):
    """
    Generate the HMAC signature of a project submission.

    Parameters
    ----------
    secret : str
        Secret HMAC key of the project, encoded in Base64.
    project_id : int
        Unique identifier of the project.
    code : str
        Content of the code file, encoded in Base64.
    dependency : str
        Content of the dependency file, encoded in Base64.

    Returns
    -------
    dict
        Dictionary containing the signature encoded in Base64
        (``signature``).
    """
    project_id_bytes = str(project_id).encode("utf-8")
    secret_bytes = base64.b64decode(secret)
    code_bytes = base64.b64decode(code)
    dependency_bytes = base64.b64decode(dependency)
    signature = generate_signature(secret_bytes, project_id_bytes, code_bytes, dependency_bytes)
    return {"signature": base64.b64encode(signature).decode("ascii")}
