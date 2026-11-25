from pydantic import BaseModel


class QualityGateModel(BaseModel):
    """
    Pydantic model of a quality gate.

    Attributes
    ----------
    status : str
        Status of the quality gate.
    """

    status: str
