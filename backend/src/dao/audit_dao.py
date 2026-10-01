from business_object.audit import Audit
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class AuditDao(metaclass=Singleton):
    """Class containing methods to access Audit in the database."""

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
    def find_by_id(self, id_audit: int) -> Audit:
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
                        "  FROM audit                       "
                        " WHERE id_audit = %(id_audit)s;   ",
                        {"id_audit": id_audit},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        audit = None
        if res:
            audit = Audit(
                id_audit=res["id_audit"],
                id_project=res["id_project"],
                date=res["date"],
                vulnerabilities=res["vulnerabilities"],
                licenses=res["licenses"],
                antipatterns=res["antipattern"],
                complexity=res["complexity"],
                energy_consumption_kwh=res["energy_consumption_kwh"],
                carbon_emission_gco2e=res["carbon_emission_gco2e"],
                sbom=res["sbom"],
                quality_gate=res["quality_gate"],
            )

        return audit

    @log
    def find_all(self) -> list[Audit]:
        """List all audits in the database.
        Returns:
            list[Audit] sorted by username
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                "
                        "  FROM audit                           "
                        " ORDER BY username;                     "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        users_list = []

        if res:
            for row in res:
                audit = Audit(
                    id_audit=row["id_audit"],
                    id_project=row["id_project"],
                    date=row["date"],
                    vulnerabilities=row["vulnerabilities"],
                    licenses=row["licenses"],
                    antipatterns=row["antipattern"],
                    complexity=row["complexity"],
                    energy_consumption_kwh=row["energy_consumption_kwh"],
                    carbon_emission_gco2e=row["carbon_emission_gco2e"],
                    sbom=row["sbom"],
                    quality_gate=row["quality_gate"],
                )

                users_list.append(audit)

        return users_list

    @log
    def update(self, audit) -> bool:
        """Update a audit in the database.
        Args:
            Audit to be updated
        Returns:
            True if update is successful, False otherwise
        """
        nb_affected_rows = 0

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE audit                                                  "
                        "   SET username = %(username)s,                                "
                        "       password = COALESCE(%(password)s, password),            "
                        "       email = %(email)s,                                      "
                        "       access_token = COALESCE(%(access_token)s, access_token) "
                        " WHERE id_user = %(id_user)s;                              ",
                        {
                            "username": audit.username,
                            "password": audit.password,
                            "email": audit.email,
                            "access_token": audit.access_token,
                            "id_user": audit.id_user,
                        },
                    )
                    nb_affected_rows = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return nb_affected_rows == 1

    @log
    def delete(self, audit) -> bool:
        """Delete a audit from the database.
        Args:
            Audit to delete from the database
        Returns:
            True if the audit was successfully deleted, False otherwise
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM audit                               "
                        " WHERE id_user = %(id_user)s                 ",
                        {"id_user": audit.id_user},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return res > 0

    @log
    def login(self, username: str, password: str) -> Audit:
        """Login using username and password.
        Args:
            username (str)
            password (str)
        Returns:
            Audit or None
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                               "
                        "  FROM audit                          "
                        " WHERE username = %(username)s         "
                        "   AND password = %(password)s;        ",
                        {"username": username, "password": password},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        audit = None

        if res:
            audit = Audit(
                username=res["username"],
                password=res["password"],
                email=res["email"],
                access_token=res["access_token"],
                id_player=res["id_player"],
            )

        return audit

    @log
    def find_by_token(self, access_token: str) -> Audit:
        """Find a audit by their access token.
        Args:
            access_token (str): The token to search for.
        Returns:
            Audit object if found, otherwise None.
        """
        if not access_token:
            return None

        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                "
                        "  FROM audit                           "
                        " WHERE access_token = %(token)s;        ",
                        {"token": access_token},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(f"Error finding audit by token: {e}")
            raise

        audit = None
        if res:
            audit = Audit(
                id_player=res["id_player"],
                username=res["username"],
                password=res["password"],
                email=res["email"],
                access_token=res["access_token"],
            )

        return audit
