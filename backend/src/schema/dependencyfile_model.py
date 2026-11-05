from pydantic import BaseModel


class DependencyFileModel(BaseModel):
    name: str
    content: str
    type_file: str
