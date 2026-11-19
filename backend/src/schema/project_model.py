# from hmac import HMAC -> on converti la clé en bytes en str
from pydantic import BaseModel

from schema.codefile_model import CodeFileModel
from schema.dependencyfile_model import DependencyFileModel


class ProjectReadModel(BaseModel):
    """
    Model returned when the user consults a project.

    Attributes
    ----------
    id_project : int
        Unique identifier of the project.
    name_project : str
        Name of the project.
    """
    id_project: int
    name_project: str


class ProjectResponseModel(BaseModel):
    """
    Model returned when a project is created.

    Attributes
    ----------
    id_project : int
        Unique identifier of the project.
    name_project : str
        Name of the project.
    secretHMACkey : str
        Secret HMAC key of the project, encoded in Base64.
    """
    id_project: int
    name_project: str
    secretHMACkey: str


class ProjectCreateModel(BaseModel):
    """
    Model used to create or rename a project.

    Attributes
    ----------
    name_project : str
        Name of the project.
    """
    name_project: str


class ProjectCompletedModel(BaseModel):
    """
    Project sent with its files to be audited.

    Attributes
    ----------
    id_project : int
        Unique identifier of the project.
    codefile : CodeFileModel
        Code file of the project.
    dependencyfile : DependencyFileModel
        Dependency file of the project.
    """
    id_project: int
    codefile: CodeFileModel
    dependencyfile: DependencyFileModel
