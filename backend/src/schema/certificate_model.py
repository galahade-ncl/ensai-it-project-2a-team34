from datetime import datetime

from pydantic import BaseModel


class CertificateModel(BaseModel):
    name: str
    date: datetime
    type_file: str
    status: str
    content: bytes
