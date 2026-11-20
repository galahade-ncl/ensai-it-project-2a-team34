import hmac

from business_object.audit import Audit
from business_object.project import Project
from business_object.user import User
from dao.audit_dao import AuditDao
from dao.project_dao import ProjectDao
from utils.log_utils import log
from utils.security import encode_secret_key, generate_secret_HMAC_key, generate_signature


class ProjectService:
    """
    Service that handles business logic related to a project (upload, update, etc.).
    """

    @log
    def upload(self, project_name: str, user: User) -> Project | None:
        """
        Create a new project in the system.

        A new secret HMAC key is generated for the project.

        Parameters
        ----------
        project_name : str
            Name of the project.
        user : User
            User that owns the project.

        Returns
        -------
        Project or None
            The created project, or None if the creation failed.
        """
        secret_HMAC_key = generate_secret_HMAC_key()
        new_project = Project(name_project=project_name, secretHMACkey=secret_HMAC_key)
        return new_project if ProjectDao().create(new_project, user.id_user) else None

    @log
    def find_by_id(self, id_project: int) -> Project | None:
        """
        Find a project by its unique identifier.

        Parameters
        ----------
        id_project : int
            Identifier of the project.

        Returns
        -------
        Project or None
            The project if found, otherwise None.
        """
        return ProjectDao().find_by_id(id_project)

    @log
    def find_by_id_and_user(self, id_project: int, id_user: int) -> Project | None:
        """
        Find a project by its identifier, only if it belongs to the given user.

        Parameters
        ----------
        id_project : int
            Identifier of the project.
        id_user : int
            Identifier of the user.

        Returns
        -------
        Project or None
            The project if found and owned by the user, otherwise None.
        """
        return ProjectDao().find_by_id_and_user(id_project, id_user)

    @log
    def update(self, project: Project) -> Project | None:
        """
        Update an existing project's information.

        Parameters
        ----------
        project : Project
            Project containing the updated information.

        Returns
        -------
        Project or None
            The updated project, or None if the update failed.
        """
        return project if ProjectDao().update(project) else None

    @log
    def delete(self, project: Project) -> bool:
        """
        Delete a project.

        Parameters
        ----------
        project : Project
            Project to delete.

        Returns
        -------
        bool
            True if the deletion was successful, False otherwise.
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
        Verify the HMAC signature sent with a project.

        Parameters
        ----------
        project : Project
            Project related to the signature, with its files.
        signature : bytes
            Signature to verify.

        Returns
        -------
        bool
            True if the signature is valid, False otherwise.
        """
        code = project.codefile.content
        dependency = project.dependencyfile.content
        project_id = str(project.id_project).encode("utf-8")

        expected_signature = generate_signature(project.secretHMACkey, project_id, code, dependency)

        return hmac.compare_digest(expected_signature, signature)

    @log
    def list_all_audit(self, id_project: int) -> list[Audit] | None:
        """
        List all the audits of a project.

        Parameters
        ----------
        id_project : int
            Identifier of the project.

        Returns
        -------
        list of Audit or None
            Audits of the project, or None if the project does not exist.
        """
        # Find the audits corresponding to the project id
        project = ProjectService().find_by_id(id_project)
        if not project:
            return None
        return AuditDao().list_all_audit(project)

    @log
    def regenerate_secret_key(self, project: Project) -> str | None:
        """
        Generate and store a new secret key for the project.

        Parameters
        ----------
        project : Project
            Project whose secret key is regenerated.

        Returns
        -------
        str or None
            The new key encoded in Base64, or None if the update failed.
        """
        project.secretHMACkey = generate_secret_HMAC_key()
        if not ProjectDao().update_secret_key(project):
            return None
        return encode_secret_key(project.secretHMACkey)
