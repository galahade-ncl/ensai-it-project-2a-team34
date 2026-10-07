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
        """Finds a specific file by their unique id.
        Args:
            id_file (int) : id of the file
        Returns:
            File object if found, otherwise None.
        """
        return FileDao().find_by_id(id_file)

    @log
    def find_all_by_project(self, id_project: int) -> list[File]:
        """List all file related to the project corresponding with the id.
        Args:
            id_project (int) : id of the project
        Returns:
            list[File]
        """
        return FileDao().find_all_by_project(id_project)

    @log
    def find_user(self, id_file: int) -> User:
        pass

    @log
    def find_project(self, id_file: int) -> Project:
        pass

    @log
    def update(self, file: File) -> File:
        """
        Updates an existing file's information.
        Args:
            File object containing updated information.
        Returns:
            The updated File object, or None if the update failed.
        """
        return file if FileDao().update(file) else None

    @log
    def delete(self, file: File) -> bool:
        """Delete a file.
        Args:
            File object to be deleted.
        Returns:
            True if deletion was successful, False otherwise.
        """
        return FileDao().delete(file)

    # Utilité de la méthode ?
    @log
    def get_content(self, file: File) -> bool:
        return file.get_content()
