from pydantic import BaseModel, ConfigDict


class LicenceModel(BaseModel):
    """
    Pydantic model of a licence.

    Attributes
    ----------
    id_licence : int or None
        Unique identifier of the licence.
    name : str
        Name of the licence (SPDX identifier).
    risk_level : str
        Risk level associated with the licence.
    """

    model_config = ConfigDict(from_attributes=True)

    id_licence: int | None = None
    name: str
    risk_level: str
