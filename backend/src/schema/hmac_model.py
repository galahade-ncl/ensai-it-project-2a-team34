from pydantic import BaseModel


class HmacSignatureRequest(BaseModel):
    secret: str
    project_id: int
    code: str
    dependency: str


class HmacSignatureResponse(BaseModel):
    signature: str
