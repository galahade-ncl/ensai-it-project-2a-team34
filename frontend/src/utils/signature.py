import base64
import hashlib
import hmac


def generate_signature(secret: bytes, project_id: int, code: bytes, dependency: bytes) -> str:
    """HMAC-SHA256 signature, identical to the backend's generate_signature (base64)."""
    mac = hmac.new(secret, digestmod=hashlib.sha256)
    for part in (str(project_id).encode("utf-8"), code, dependency):
        mac.update(len(part).to_bytes(8, "big"))
        mac.update(part)
    return base64.b64encode(mac.digest()).decode("ascii")
