from pydantic import BaseModel


class CodeFileModel(BaseModel):
    """
    Code file sent by the client.

    Attributes
    ----------
    name : str
        Name of the file.
    content : str
        Content of the file, encoded in Base64.
    type_file : str
        Extension of the file.
    """

    name: str
    content: str
    type_file: str
