import hmac

from business_object.audit import Audit
from business_object.project import Project
from business_object.user import User
from dao.audit_dao import AuditDao
from dao.project_dao import ProjectDao
from utils.log_utils import log
from utils.security import generate_secret_HMAC_key, generate_signature


class ProjectService:
    """Service that handles business logic related to a project (upload, update, etc.)."""

    @log
    def upload(self, project_name: str, user: User) -> Project | None:
        """Creates a new project in the system.
        Args:
            name_project (str) : name of the project
            user (User) : user that owns the project
        Returns:
            Project object created or None if creation failed.
        """
        secret_HMAC_key = generate_secret_HMAC_key()
        new_project = Project(name_project=project_name, secretHMACkey=secret_HMAC_key)
        return new_project if ProjectDao().create(new_project, user.id_user) else None

    @log
    def find_by_id(self, id_project: int) -> Project | None:
        """Finds a specific project by their unique id.
        Args:
            id_project (int) : id of the project
        Returns:
            Project object if found, otherwise None.
        """
        return ProjectDao().find_by_id(id_project)

    @log
    def find_by_id_and_user(self, id_project: int, id_user: int) -> Project | None:
        """Finds a project by its id only if it belongs to the given user.
        Args:
            id_project (int) : id of the project
            id_user (int) : id of the user
        Returns:
            Project object if found and owned by the user, otherwise None.
        """
        return ProjectDao().find_by_id_and_user(id_project, id_user)

    @log
    def update(self, project: Project) -> Project | None:
        """Updates an existing project's information.
        Args:
            Project object containing updated information.
        Returns:
            The updated Project object, or None if the update failed.
        """
        return project if ProjectDao().update(project) else None

    @log
    def delete(self, project: Project) -> bool:
        """Delete a project.
        Args:
            Project object to be deleted.
        Returns:
            A booléan object: True if the deletion was successful, False otherwise.
        """
        return ProjectDao().delete(project)

    # @log
    # def get_secretHMACkey(id_project: int) -> bytes:
    #     """DOC A FAIRE"""
    #     return ProjectDao().get_secretHMACkey(id_project=id_project)

    @staticmethod
    @log
    def verify_signature(project: Project, signature: bytes) -> bool:
        """
        Verify the signature given
        Args:
            project (Project): Project related to the signature
            signature (bytes): the signature given
        Returns:
            Boolean object indicating whether the signature is valid or not
        """
        code = project.codefile.content
        dependency = project.dependencyfile.content
        project_id = str(project.id_project).encode("utf-8")

        expected_signature = generate_signature(project.secretHMACkey, project_id, code, dependency)

        return hmac.compare_digest(expected_signature, signature)

    @log
    def list_all_audit(self, id_project: int) -> list[Audit] | None:
        """List all audits on the project corresponding with the id.
        Args:
            id_project (int) : id of the project
        Returns:
            A list of Audits on the project"""
        # Find the audits corresponding to the project id
        project = ProjectService().find_by_id(id_project)
        if not project:
            return None
        return AuditDao().list_all_audit(project)
