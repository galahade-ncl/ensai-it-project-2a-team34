from hmac import HMAC

from pydantic import BaseModel

from business_object.user import User


class ProjectReadModel(BaseModel):
    id_project: int
    name_project: str
    user: User



class ProjectResponseModel(BaseModel):
    id_project: int
    name_project: str
    user: User
    secretHMACkey: HMAC


class ProjectCreateModel(BaseModel):
    name_project: str
    user: User
