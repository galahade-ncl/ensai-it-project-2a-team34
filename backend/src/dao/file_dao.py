from business_object.file.codefile import CodeFile
from business_object.file.dependencyfile import DependencyFile
from business_object.file.file import File
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class FileDao(metaclass=Singleton):
    """Class containing methods to access Files in the database."""

    @log
    def create(self, file: File, id_project: int) -> bool:
        """Create a file in the database.
        Args:
            File to create
        Returns:
            True if creation is successful, False otherwise
        """
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO file(path) VALUES (%(path)s) RETURNING id_file;",
                        {
                            "path": file.path,
                            "type": file.get_type(),
                            "project_file": id_project,
                            "name_file": file.name,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            file.id_file = res["id_file"]
            file.date = res["date"]
            created = True

        return created

    @log
    def find_by_id(self, id_file: int) -> File:
        """Find a file by its id.
        Args:
            id_file (int): The ID of the file to find
        Returns:
            File matching the given id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "FROM file                     "
                        "WHERE id_file = %(id_file)s;   ",
                        {"id_file": id_file},
                    )
                    res_file = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        file = None
        if res_file["type"] == "code":
            file = CodeFile(
                id_file=res_file["id_file"],
                name=res_file["name_file"],
                date=res_file["date"],
                path=res_file["path"],
            )

        if res_file["type"] == "dependency":
            return DependencyFile(
                id_file=res_file["id_file"],
                name=res_file["name_file"],
                date=res_file["date"],
                path=res_file["path"],
                dependencies=[],
            )

        return file

    @log
    def find_all_by_project(self, id_project: int) -> list[File]:
        """List all file of the project from the ID.
        Returns:
            list[File]
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                "
                        "  FROM file                           "
                        "WHERE project_file = %(id_proj)s;   ",
                        {"id_proj": id_project},
                    )
                    res_files = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        file_list = []

        if res_files:
            for row in res_files:
                if row["type"] == "code":
                    file = CodeFile(
                        id_file=row["id_file"],
                        name=row["name_file"],
                        date=row["date"],
                        path=row["path"],
                    )

                elif row["type"] == "dependency":
                    file = DependencyFile(
                        id_file=row["id_file"],
                        name=row["name_file"],
                        date=row["date"],
                        path=row["path"],
                        dependencies=[],
                    )

                file_list.append(file)

        return file_list

    @log
    def update(self, file: File, id_project: int) -> bool:
        """Update a file in the database.
        Args:
            File to be updated
        Returns:
            True if update is successful, False otherwise
        """
        nb_affected_rows = 0

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE file                                                  "
                        "   SET name_file = %(name_file)s,                                      "
                        "       path = %(path)s,                                      "
                        "       date = %(date)s,                                      "
                        "       type_file = %(type_file)s "
                        "       project_file = %(project_file)s "
                        " WHERE id_file = %(id_file)s;                              ",
                        {
                            "name_file": file.name,
                            "path": file.path,
                            "date": file.date,
                            "type_file": file.get_type(),
                            "project_file": id_project,
                        },
                    )
                    nb_affected_rows = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return nb_affected_rows == 1

    @log
    def delete(self, file: File) -> bool:
        """Delete a file from the database.
        Args:
            File to delete from the database
        Returns:
            True if the file was successfully deleted, False otherwise
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM file                               "
                        " WHERE id_file = %(id_file)s                 ",
                        {"id_file": file.id_file},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return res > 0
