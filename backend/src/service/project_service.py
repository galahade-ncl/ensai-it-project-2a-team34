from business_object.project import Project
from business_object.user import User
from dao.project_dao import ProjectDao


class ProjectService:
    """Service that handles business logic related to a project (upload, update, etc.)."""

    @log
    def upload(self, project_name: str, user: User) -> Project:
        """Creates a new project in the system.
        Args:
            name_project (str) : name of the project
            user (User) : user that owns the project
        Returns:
            Project object created or None if creation failed.
        """
        secret_HMAC_key = generate_secret_HMAC_key(self)
        new_project = Project(
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
