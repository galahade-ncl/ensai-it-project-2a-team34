from business_object.project import Project
from business_object.user import User
from business_object.file.file import File
from dao.project_dao import ProjectDao


class FileService:
    """Service that handles business logic related to a project (upload, update, etc.)."""

    @log
    def upload(self, file_name: str, id_project: int, type: str) -> File:
        """Creates a new file in the system.
        Args:
            file_name (str) : name of the file
            id_project (int) : id of the project that owns the file
        Returns:
            File object created or None if creation failed.
        """
        if type == "dependency":
            new_file = DependencyFile(
                name_project=project_name,
                user=user,
                secretHMACkey=secret_HMAC_key
            )
        return new_project if ProjectDao().create(new_project) else None


    @log
    def find_by_id(self, id_project: int):
        pass

    @log
    def list_all_project(self, id_user: int):
        pass

    @log
    def update(self, project: Project):
        pass

    @log
    def delete(self, project: Project):
        pass

    @log
    def generate_secret_HMAC_key(self):
        """ generate a new secret key """
        pass

    @log
    def verify_signature(self, project: Project, signature: bytes):
        pass
