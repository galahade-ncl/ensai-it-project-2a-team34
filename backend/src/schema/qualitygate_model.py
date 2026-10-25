from pydantic import BaseModel


class QualityGateModel(BaseModel):
    status: str
