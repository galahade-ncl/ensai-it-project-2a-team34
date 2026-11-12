import base64

from fastapi import APIRouter

from utils.log_utils import get_logger
from utils.security import generate_signature

router = APIRouter()

logger = get_logger(__name__)


@router.post("/hmac/key")
async def create_hmac_key(secret, project_id, code, dependency):
    project_id_bytes = str(project_id).encode("utf-8")
    secret_bytes = base64.b64decode(secret)
    code_bytes = base64.b64decode(code)
    dependency_bytes = base64.b64decode(dependency)
    signature = generate_signature(secret_bytes, project_id_bytes, code_bytes, dependency_bytes)
    return {"signature": base64.b64encode(signature).decode("ascii")}
