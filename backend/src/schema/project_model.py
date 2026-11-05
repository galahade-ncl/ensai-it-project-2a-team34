# from hmac import HMAC -> on converti la clé en bytes en str
from pydantic import BaseModel

from schema.codefile_model import CodeFileModel
from schema.dependencyfile_model import DependencyFileModel


class ProjectReadModel(BaseModel):
    id_project: int
    name_project: str


class ProjectResponseModel(BaseModel):
    id_project: int
    name_project: str
    secretHMACkey: str


class ProjectCreateModel(BaseModel):
    name_project: str


class ProjectCompletedModel(BaseModel):
    id_project: int
    codefile: CodeFileModel
    dependencyfile: DependencyFileModel
