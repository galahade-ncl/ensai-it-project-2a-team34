from pydantic import BaseModel, ConfigDict


class LicenceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_licence: int | None = None
    name: str
    risk_level: str
