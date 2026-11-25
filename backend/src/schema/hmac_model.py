from pydantic import BaseModel


class HmacSignatureRequest(BaseModel):
    """
    Request body to compute the HMAC signature of an audit request.

    Attributes
    ----------
    secret : str
        Secret HMAC key of the project, encoded in Base64.
    project_id : int
        Unique identifier of the project.
    code : str
        Content of the code file, encoded in Base64.
    dependency : str
        Content of the dependency file, encoded in Base64.
    """
    secret: str
    project_id: int
    code: str
    dependency: str


class HmacSignatureResponse(BaseModel):
    """
    Response body containing the computed HMAC signature.

    Attributes
    ----------
    signature : str
        HMAC signature of the request, encoded in Base64.
    """
    signature: str
