from business_object.project import Project
from dao.db_connection import DBConnection
from dao.user_dao import UserDao
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class ProjectDao(metaclass=Singleton):
    """Class containing methods to access Projects in the database."""

    @log
    def create(self, project: Project) -> bool:
        """
        Create a project in the database.

        Arguments
        ---------
        project : Project
            Project to create

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
                        "INSERT INTO project(name_project, id_user, secretHMACkey) VALUES "
                        "(%(name_project)s, %(id_user)s, %(secretHMACkey)s) "
                        "RETURNING id_project;",
                        {
                            "name_project": project.name_project,
                            "id_user": project.user.id_user,
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
                        "SELECT * "
                        "  FROM project "
                        " WHERE id_project = %(id_project)s;",
                        {"id_project": id_project},
                    )
                    res_project = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        project = None
        if res_project:
            user = UserDao().find_by_id(res_project["id_user"])
            project = Project(
                id_project=res_project["id_project"],
                name_project=res_project["name_project"],
                user=user,
                secretHMACkey=res_project["secrethmackey"],
            )

        return project

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
                        "UPDATE project "
                        "   SET name_project = %(name_project)s, "
                        "       id_user = %(id_user)s, "
                        "       secretHMACkey = COALESCE(%(secretHMACkey)s, secretHMACkey) "
                        " WHERE id_project = %(id_project)s;",
                        {
                            "name_project": project.name_project,
                            "id_user": project.user.id_user,
                            "secretHMACkey": project.secretHMACkey,
                            "id_project": project.id_project,
                        },
                    )
                    nb_affected_rows = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return nb_affected_rows == 1

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
                        "DELETE FROM project WHERE id_project = %(id_project)s;",
                        {"id_project": project.id_project},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return res > 0
