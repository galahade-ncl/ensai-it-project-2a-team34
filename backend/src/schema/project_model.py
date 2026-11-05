# from hmac import HMAC -> on converti la clé en bytes en str
from pydantic import BaseModel

from schema.codefile_model import CodeFileModel
from schema.dependencyfile_model import DependencyFileModel
from schema.user_model import UserResponseModel


class ProjectReadModel(BaseModel):
    id_project: int
    name_project: str
    user: UserResponseModel


class ProjectResponseModel(BaseModel):
    id_project: int
    name_project: str
    user: UserResponseModel
    secretHMACkey: str


class ProjectCreateModel(BaseModel):
    name_project: str
    user: UserResponseModel


class ProjectCompletedModel(BaseModel):
    id_project: int
    codefile: CodeFileModel
    dependencyfile: DependencyFileModel
