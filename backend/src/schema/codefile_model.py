from pydantic import BaseModel


class CodeFileModel(BaseModel):
    name: str
    content: str
    type_file: str
