from datetime import datetime

from pydantic import BaseModel


class CertificateModel(BaseModel):
    id_certificate: int
    date: datetime
    type: str
    status: str
    path: str
