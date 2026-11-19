from fastapi import APIRouter

from schema.certificate_model import CertificateVerifyResponseModel, SignedCertificateModel
from service.certificate_service import CertificateService
from utils.security import get_key_id, get_public_key_pem

router = APIRouter()


@router.get("/.well-known/public-key", tags=["Certificates"])
def get_public_key():
    """
    Expose the public key used to sign the certificates.

    Returns
    -------
    dict
        Dictionary containing the key identifier (``kid``), the signing
        algorithm (``alg``) and the public key in PEM format
        (``public_key``).
    """
    return {"kid": get_key_id(), "alg": "Ed25519", "public_key": get_public_key_pem()}


@router.post(
    "/certificate/verify", response_model=CertificateVerifyResponseModel, tags=["Certificates"]
)
def verify_certificate(cert: SignedCertificateModel):
    """
    Verify the signature of a certificate.

    Parameters
    ----------
    cert : SignedCertificateModel
        Signed certificate to verify (content of the QR code).

    Returns
    -------
    CertificateVerifyResponseModel
        Result of the verification: ``valid=True`` with the payload if
        the signature is correct, ``valid=False`` with a reason otherwise.
    """
    if CertificateService.verify_certificate(cert.model_dump()):
        return CertificateVerifyResponseModel(valid=True, payload=cert.payload)
    return CertificateVerifyResponseModel(valid=False, reason="Invalid signature or unknown key.")
