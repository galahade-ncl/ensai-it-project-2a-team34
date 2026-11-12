from fastapi import APIRouter

from schema.certificate_model import CertificateVerifyResponseModel, SignedCertificateModel
from service.certificate_service import CertificateService
from utils.security import get_key_id, get_public_key_pem

router = APIRouter()


@router.get("/.well-known/public-key", tags=["Certificates"])
def get_public_key():
    return {"kid": get_key_id(), "alg": "Ed25519", "public_key": get_public_key_pem()}


@router.post(
    "/certificate/verify", response_model=CertificateVerifyResponseModel, tags=["Certificates"]
)
def verify_certificate(cert: SignedCertificateModel):
    if CertificateService.verify_certificate(cert.model_dump()):
        return CertificateVerifyResponseModel(valid=True, payload=cert.payload)
    return CertificateVerifyResponseModel(valid=False, reason="Invalid signature or unknown key.")
