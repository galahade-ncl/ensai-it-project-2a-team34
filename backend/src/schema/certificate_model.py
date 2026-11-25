from datetime import datetime

from pydantic import BaseModel


class SignedCertificateModel(BaseModel):
    """
    Signed certificate: what the QR code contains.

    Attributes
    ----------
    payload : dict
        Signed data of the certificate.
    kid : str
        Identifier of the key used to sign.
    alg : str
        Signing algorithm (``'Ed25519'``).
    signature : str
        Signature of the payload.
    """

    payload: dict
    kid: str
    alg: str
    signature: str


class CertificateModel(BaseModel):
    """
    Certificate returned with an audit.

    Attributes
    ----------
    name : str
        Name of the certificate.
    type_file : str
        Format of the certificate file.
    date : datetime
        Generation date of the certificate.
    signed_data : SignedCertificateModel or None
        Signed data of the certificate.
    """

    name: str
    type_file: str
    date: datetime
    signed_data: SignedCertificateModel | None = None


class CertificateVerifyResponseModel(BaseModel):
    """
    Result of the verification of a certificate.

    Attributes
    ----------
    valid : bool
        True if the signature of the certificate is valid.
    payload : dict or None
        Payload of the certificate if valid.
    reason : str or None
        Reason of the failure if not valid.
    """

    valid: bool
    payload: dict | None = None
    reason: str | None = None
