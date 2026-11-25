import base64
import binascii

from fastapi import APIRouter, Depends, HTTPException

from schema.hmac_model import HmacSignatureRequest, HmacSignatureResponse
from utils.log_utils import get_logger
from utils.security import generate_signature, verify_token

router = APIRouter()

logger = get_logger(__name__)


@router.post("/signature", response_model=HmacSignatureResponse, tags=["Hmac"])
async def create_hmac_signature(body: HmacSignatureRequest, user=Depends(verify_token)):
    """
    Compute the HMAC signature expected by POST /audit for the given files.

    Parameters
    ----------
    body : HmacSignatureRequest
        Request body containing the following fields:
        - secret : str
            Secret HMAC key of the project, encoded in Base64.
        - project_id : int
            Unique identifier of the project.
        - code : str
            Content of the code file, encoded in Base64.
        - dependency : str
            Content of the dependency file, encoded in Base64.
    user : User
        Authenticated user obtained through token verification.

    Returns
    -------
    dict
        Dictionary containing the signature encoded in Base64
        (``signature``).

    Raises
    ------
    HTTPException
        400 error if one of the Base64 fields contains invalid content.
        401 error if the authentication token is invalid or missing.
    """
    try:
        secret = base64.b64decode(body.secret, validate=True)
        code = base64.b64decode(body.code, validate=True)
        dependency = base64.b64decode(body.dependency, validate=True)
    except (binascii.Error, ValueError):
        raise HTTPException(status_code=400, detail="Invalid Base64 content.") from None

    signature = generate_signature(secret, str(body.project_id).encode("utf-8"), code, dependency)
    return {"signature": base64.b64encode(signature).decode("ascii")}
