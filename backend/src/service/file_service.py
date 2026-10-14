from business_object.file.codefile import CodeFile
from business_object.file.dependencyfile import DependencyFile
from business_object.file.file import File
from business_object.project import Project
from business_object.user import User
from dao.project_dao import FileDao
from utils.log_utils import log


class FileService:
    """Service that handles business logic related to a project (upload, update, etc.)."""

    # Utilité de la méthode ? -> on l'utilise pour la version bytes des fichiers peut etre ? De toute façon va falloir la changer, c'est pas censé être une méthode abstraite 🫠 (ça change pas selon le file)
    @log
    def get_content(self, file: File) -> bool:
        return file.get_content()
