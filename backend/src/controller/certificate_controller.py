from fastapi import APIRouter

from schema.certificate_model import CertificateVerifyResponseModel, SignedCertificateModel
from service.certificate_service import CertificateService
from utils.security import get_key_id, get_public_key_pem

router = APIRouter()


@router.get("/.well-known/public-key", tags=["Certificates"])
def get_public_key():
    """Retrieves the public key used to verify signed certificates.
    Args:
        None.
    Returns:
        dict: containing:
            - kid: Identifier of the public key.
            - alg: Cryptographic algorithm used (Ed25519).
            - public_key: Public key in PEM format.
    """
    return {"kid": get_key_id(), "alg": "Ed25519", "public_key": get_public_key_pem()}


@router.post(
    "/certificate/verify", response_model=CertificateVerifyResponseModel, tags=["Certificates"]
)
def verify_certificate(cert: SignedCertificateModel):
    """Verifies the authenticity and signature of a signed certificate.
    Args:
        cert: Signed certificate containing the payload and its cryptographic signature.
    Returns:
        CertificateVerifyResponseModel: containing:
            - valid: Boolean indicating whether the certificate signature is valid.
            - payload: Certificate payload if the signature is valid.
            - reason: Error description if the signature is invalid.
    """
    if CertificateService.verify_certificate(cert.model_dump()):
        return CertificateVerifyResponseModel(valid=True, payload=cert.payload)
    return CertificateVerifyResponseModel(valid=False, reason="Invalid signature or unknown key.")
