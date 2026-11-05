from datetime import datetime

from pydantic import BaseModel


class CertificateModel(BaseModel):
    name: str
    content: bytes | str
    type_file: str
    date: datetime
