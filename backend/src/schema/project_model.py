# from hmac import HMAC -> renvoie un str qu'on converti en bytes

from pydantic import BaseModel

# from business_object.user import User


class ProjectReadModel(BaseModel):
    id_project: int
    name_project: str
#    user: User -> il faudrait appeler UserModel


class ProjectResponseModel(BaseModel):
    id_project: int
    name_project: str
#    user: User -> il faudrait appeler UserModel
    secretHMACkey: str


class ProjectCreateModel(BaseModel):
    name_project: str
#    user: User -> il faudrait appeler UserModel
