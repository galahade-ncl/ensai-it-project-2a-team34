from business_object.project import Project
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class ProjectDao(metaclass=Singleton):
    """Class containing methods to access Projects in the database."""

    @log
    def create(self, project: Project, id_user: int) -> bool:
        """
        Create a project in the database.

        Arguments
        ---------
        project : Project
            Project to create
        id_user : int
            The ID of the user who owns the project

        Returns
        -------
        bool
            True if creation is successful, False otherwise
        """
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO project_table(name_project, id_user, secretHMACkey) VALUES "
                        "(%(name_project)s, %(id_user)s, %(secretHMACkey)s) "
                        "RETURNING id_project;",
                        {
                            "name_project": project.name_project,
                            "id_user": id_user,
                            "secretHMACkey": project.secretHMACkey,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            project.id_project = res["id_project"]
            created = True

        return created

    @log
    def find_by_id(self, id_project: int) -> Project | None:
        """
        Find a project by its id.

        Arguments
        ---------
        id_project : int
            The ID of the project to find

        Returns
        -------
        Project
            Project matching the given id, or None if not found
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *   FROM project_table  WHERE id_project = %(id_project)s;",
                        {"id_project": id_project},
                    )
                    res_project = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        project = None
        if res_project:
            project = Project(
                id_project=res_project["id_project"],
                name_project=res_project["name_project"],
                secretHMACkey=bytes(res_project["secrethmackey"]),
            )

        return project

    @log
    def find_by_id_and_user(self, id_project: int, id_user: int) -> Project | None:
        """
        Find a project by its id, only if it belongs to the given user.

        Arguments
        ---------
        id_project : int
            The ID of the project to find
        id_user : int
            The ID of the user who must own the project

        Returns
        -------
        Project
            Project matching the given id owned by the given user, or None if not found
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM project_table WHERE id_project = %(id_project)s AND id_user = %(id_user)s;",
                        {"id_project": id_project, "id_user": id_user},
                    )
                    res_project = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        project = None
        if res_project:
            project = Project(
                id_project=res_project["id_project"],
                name_project=res_project["name_project"],
                secretHMACkey=bytes(res_project["secrethmackey"]),
            )

        return project

    @log
    def list_all_project(self, id_user: int) -> list[Project]:
        """
        List all projects belonging to a given user.

        Arguments
        ---------
        id_user : int
            The ID of the user whose projects are to be listed

        Returns
        -------
        list[Project]
            List of the user's projects, or an empty list if there are none
        """
        res = []

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM project_table WHERE id_user = %(id_user)s ORDER BY id_project;",
                        {"id_user": id_user},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        projects = []
        for row in res:
            projects.append(
                Project(
                    id_project=row["id_project"],
                    name_project=row["name_project"],
                    secretHMACkey=bytes(row["secrethmackey"]),
                )
            )

        return projects

    @log
    def update(self, project: Project) -> bool:
        """
        Update a project in the database.

        Arguments
        ---------
        project : Project
            Project to be updated

        Returns
        -------
        bool
            True if update is successful, False otherwise
        """
        nb_affected_rows = 0

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE project_table "
                        "   SET name_project = %(name_project)s, "
                        "       secretHMACkey = COALESCE(%(secretHMACkey)s, secretHMACkey) "
                        " WHERE id_project = %(id_project)s;",
                        {
                            "name_project": project.name_project,
                            "secretHMACkey": project.secretHMACkey,
                            "id_project": project.id_project,
                        },
                    )
                    nb_affected_rows = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return nb_affected_rows == 1

    # @log
    # def get_secretHMACkey(self, id_project: int) -> str | None:
    #     """
    #     Retrieve the secret HMAC key for a specific project.

    #     Arguments
    #     ---------
    #     id_project : int
    #         The ID of the project

    #     Returns
    #     -------
    #     str | None
    #         The secret HMAC key if found, None otherwise
    #     """
    #     try:
    #         with DBConnection().connection as connection:
    #             with connection.cursor() as cursor:
    #                 cursor.execute(
    #                     "SELECT secretHMACkey FROM project_table WHERE id_project = %(id_project)s;",
    #                     {"id_project": id_project},
    #                 )
    #                 res = cursor.fetchone()
    #     except Exception as e:
    #         logger.error(e)
    #         raise

    #     if res:
    #         return res["secretHMACkey"]

    #     return None

    @log
    def delete(self, project: Project) -> bool:
        """
        Delete a project from the database.

        Arguments
        ---------
        project : Project
            Project to delete

        Returns
        -------
        bool
            True if the project was deleted, False otherwise
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM project_table WHERE id_project = %(id_project)s;",
                        {"id_project": project.id_project},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return res > 0
