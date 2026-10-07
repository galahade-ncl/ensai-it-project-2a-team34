from pydantic import BaseModel


class ProjectModel(BaseModel):
    id_project: int
    name_project: str
