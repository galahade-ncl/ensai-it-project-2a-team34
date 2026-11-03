# from hmac import HMAC -> on converti la clé en bytes en str
from pydantic import BaseModel

from schema.user_model import UserModel


class ProjectReadModel(BaseModel):
    id_project: int
    name_project: str
    user: UserModel


class ProjectResponseModel(BaseModel):
    id_project: int
    name_project: str
    user: UserModel
    secretHMACkey: str


class ProjectCreateModel(BaseModel):
    name_project: str
    user: UserModel
