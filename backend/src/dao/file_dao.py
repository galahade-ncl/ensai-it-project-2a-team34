from business_object.file import File
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class FileDao(metaclass=Singleton):
    """Class containing methods to access Files in the database."""

    @log
    def create(self, file) -> bool:
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
                        "INSERT INTO file(path) VALUES "
                        "(%(path)s) "
                        "RETURNING id_file;",
                        {
                            "path": file.path,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            file.id_file = res["id_file"]
            created = True

        return created
