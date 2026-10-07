from business_object.file.codefile import CodeFile
from business_object.file.dependencyfile import DependencyFile
from business_object.file.file import File
from business_object.project import Project
from business_object.user import User
from dao.project_dao import FileDao
from utils.log_utils import log


class FileService:
    """Service that handles business logic related to a project (upload, update, etc.)."""

    @log
    def upload(self, file_name: str, type: str, id_project: int) -> File:
        """Creates a new file in the system (dependencyfile or codefile).
        Args:
            file_name (str) : name of the file
            type (str) : type of the file
            id_project (int) : id of the project that owns the file
        Returns:
            File object created or None if creation failed.
        """
        if type == "dependency":
            new_file = DependencyFile(name=file_name, path=File.get_path(), dependencies=[])
        elif type == "code":
            new_file = CodeFile(name=file_name, path=File.get_path())
        else:
            # Est-ce qu'on return vraiment None ici ? Ou une erreur ?
            return None
        return new_file if FileDao().create(new_file) else None

    @log
    def find_by_id(self, id_file: int) -> File:
        pass

    @log
    def find_all_by_project(self, id_project: int) -> list[File]:
        pass

    @log
    def find_user(self, id_file: int) -> User:
        pass

    @log
    def find_project(self, id_file: int) -> Project:
        pass

    @log
    def update(self, file: File) -> File:
        """generate a new secret key"""
        pass

    @log
    def delete(self, File) -> bool:
        pass

    @log
    def get_content(self) -> bool:
        pass
