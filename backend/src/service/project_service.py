import hmac

from business_object.project import Project
from business_object.user import User
from dao.project_dao import ProjectDao
from utils.log_utils import log
from utils.security import generate_secret_HMAC_key, generate_signature


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
        new_project = Project(name_project=project_name, user=user, secretHMACkey=secret_HMAC_key)
        return new_project if ProjectDao().create(new_project) else None

    @log
    def find_by_id(self, id_project: int):
        """Finds a specific project by their unique id.
        Args:
            id_project (int) : id of the project
        Returns:
            Project object if found, otherwise None.
        """
        return ProjectDao().find_by_id(id_project)

    @log
    def list_all_project(self, id_user: int):
        """List all projects owned by the user corresponding with the id.
        Args:
            id_user (int) : id of the user
        Returns:
            list[Project]"""
        return ProjectDao().find_all_project(id_user)

    @log
    def update(self, project: Project):
        """Updates an existing project's information.
        Args:
            Project object containing updated information.
        Returns:
            The updated Project object, or None if the update failed.
        """
        return project if ProjectDao().update(project) else None

    @log
    def delete(self, project: Project):
        """Delete a project.
        Args:
            Project object to be deleted.
        Returns:
            True if deletion was successful, False otherwise.
        """
        return ProjectDao().delete(project)

    # Est-ce qu'on garde la méthode là ?
    @log
    def verify_signature(project: Project, code: bytes, dependency: bytes, signature: bytes) -> bool:
        """
        Verify the signature given
        Args:
            project (Project): Project related to the signature
            code (bytes): The binary version of a codefile
            dependency (bytes): The binary version of a dependencyfile,
            signature (bytes): the signature given
        Returns:
            Boolean object indicating whether the signature is valid or not
        """
        expected_signature = generate_signature(project.secretHMACkey, code, dependency)

        return hmac.compare_digest(expected_signature, signature)
