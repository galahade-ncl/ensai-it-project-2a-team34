from business_object.project import Project
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class ProjectDao(metaclass=Singleton):
    """Class containing methods to access Projects in the database."""

    @log
    def create(self, project: Project) -> bool:
        """Create a project in the database.
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
    def find_by_id(self, id_project: int) -> Project:
        """Find a project by its id.
        Args:
            id_project (int): The ID of the project to find
        Returns:
            Project matching the given id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "FROM project                     "
                        "WHERE id_project = %(id_project)s;   ",
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
                user=res_project["user"],
                codefile=res_project["codefile"],
                dependencyfile=res_project["dependencyfile"],
                secretHMACkey=res_project["secretHMACkey"],
            )

        return project
