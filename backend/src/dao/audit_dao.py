from business_object.user import User
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class AuditDao(metaclass=Singleton):
    """Class containing methods to access Audit  in the database."""

    @log
    def create(self, audit) -> bool:
        """Create an audit in the database.
        Args:
            Audit to create
        Returns:
            True if creation is successful, False otherwise
        """
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO audit(id_project, date, complexity, energy_consumption_kwh, carbon_emission_gco2e, vulnerabilities, sbom) VALUES "
                        "(%(id_project)s, %(date)s, %(complexity)s, %(energy_consumption_kwh)s, %(carbon_emission_gco2e)s, %(vulnerabilities)s, %(sbom)s) "
                        "RETURNING id_audit;",
                        {
                            "id_project": audit.id_project,
                            "date": audit.date,
                            "complexity": audit.complexity,
                            "energy_consumption_kwh": audit.energy_consumption_kwh,
                            "carbon_emission_gco2e": audit.carbon_emission_gco2e,
                            "vulnerabilities": audit.vulnerabilities,
                            "sbom": audit.sbom,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            audit.id_audit = res["id_audit"]
            created = True

        return created

    @log
    def find_by_id(self, id_audit: int) -> User:
        """Find an audit by their id.
        Args:
            id_audit (int): The ID of the audit to find
        Returns:
            Audit matching the given id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "  FROM user                       "
                        " WHERE id_user = %(id_user)s;   ",
                        {"id_user": id_user},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        user = None
        if res:
            user = User(
                username=res["username"],
                email=res["email"],
                id_user=res["id_user"],
                password=res["password"],
            )

        return user

    @log
    def find_all(self) -> list[User]:
        """List all users in the database.
        Returns:
            list[User] sorted by username
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                "
                        "  FROM user                           "
                        " ORDER BY username;                     "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        users_list = []

        if res:
            for row in res:
                user = User(
                    id_player=row["id_player"],
                    username=row["username"],
                    password=row["password"],
                    email=row["email"],
                )

                users_list.append(user)

        return users_list

    @log
    def update(self, user) -> bool:
        """Update a user in the database.
        Args:
            User to be updated
        Returns:
            True if update is successful, False otherwise
        """
        nb_affected_rows = 0

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE user                                                  "
                        "   SET username = %(username)s,                                "
                        "       password = COALESCE(%(password)s, password),            "
                        "       email = %(email)s,                                      "
                        "       access_token = COALESCE(%(access_token)s, access_token) "
                        " WHERE id_user = %(id_user)s;                              ",
                        {
                            "username": user.username,
                            "password": user.password,
                            "email": user.email,
                            "access_token": user.access_token,
                            "id_user": user.id_user,
                        },
                    )
                    nb_affected_rows = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return nb_affected_rows == 1

    @log
    def delete(self, user) -> bool:
        """Delete a user from the database.
        Args:
            User to delete from the database
        Returns:
            True if the user was successfully deleted, False otherwise
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM user                               "
                        " WHERE id_user = %(id_user)s                 ",
                        {"id_user": user.id_user},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return res > 0

    @log
    def login(self, username: str, password: str) -> User:
        """Login using username and password.
        Args:
            username (str)
            password (str)
        Returns:
            User or None
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                               "
                        "  FROM user                          "
                        " WHERE username = %(username)s         "
                        "   AND password = %(password)s;        ",
                        {"username": username, "password": password},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        user = None

        if res:
            user = User(
                username=res["username"],
                password=res["password"],
                email=res["email"],
                access_token=res["access_token"],
                id_player=res["id_player"],
            )

        return user

    @log
    def find_by_token(self, access_token: str) -> User:
        """Find a user by their access token.
        Args:
            access_token (str): The token to search for.
        Returns:
            User object if found, otherwise None.
        """
        if not access_token:
            return None

        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                "
                        "  FROM user                           "
                        " WHERE access_token = %(token)s;        ",
                        {"token": access_token},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(f"Error finding user by token: {e}")
            raise

        user = None
        if res:
            user = User(
                id_player=res["id_player"],
                username=res["username"],
                password=res["password"],
                email=res["email"],
                access_token=res["access_token"],
            )

        return user
