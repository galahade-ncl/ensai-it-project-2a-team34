from datetime import datetime

from pydantic import BaseModel


class SignedCertificateModel(BaseModel):
    """Signed certificate: what the QR code contains."""
    payload: dict
    kid: str
    alg: str
    signature: str


class CertificateModel(BaseModel):
    """ A COMPLETER """
    name: str
    content: str
    type_file: str
    date: datetime
    signed_data: SignedCertificateModel | None = None


class CertificateVerifyResponseModel(BaseModel):
    """ A COMPLETER """
    valid: bool
    payload: dict | None = None
    reason: str | None = None
