from pydantic import BaseModel


class SbomModel(BaseModel):
    content: bytes
