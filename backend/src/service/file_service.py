import ast

from business_object.dependency import Dependency
from business_object.file.codefile import CodeFile
from business_object.file.dependencyfile import DependencyFile
from business_object.file.file import File

# from business_object.project import Project
# from business_object.user import User
from utils.log_utils import log


class FileService:
    """Service that handles business logic related to a project (upload, update, etc.)."""

    # Utilité de la méthode ? -> on l'utilise pour la version bytes des fichiers peut etre ? De toute façon va falloir la changer, c'est pas censé être une méthode abstraite 🫠 (ça change pas selon le file)
    @log
    def get_content(self, file: File) -> bool:
        return file.get_content()

    @log
    def parse_dependencies(self, dependencyfile: DependencyFile) -> list[Dependency]:
        """
        Find all the dependencies in the dependencyfile
        Args:
            dependencyfile (DependencyFile): file containing all the dependencies
        Returns:
            List of Dependency object found in the file
        """
        pass

    @log
    def parse_ast(self, code_file: CodeFile) -> ast.Module:
        pass
