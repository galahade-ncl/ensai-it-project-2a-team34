
from business_object.audit import Audit
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class AuditDao(metaclass=Singleton):
    """Class containing methods to access Audits in the database."""

    @staticmethod
    def _row_to_audit(row: dict) -> Audit:
        """Convert a database row into an Audit object."""
        return Audit(
            id_audit=row["id_audit"],
            id_project=row["id_project"],
            date=row["date"],
            vulnerabilities=[],
            licenses=[],
            anti_patterns=[],
            complexity=row["complexity"],
            energy_consumption_kwh=row["energy_comsumption"],
            carbon_emission_gco2e=row["carbon_emission_gco2e"],
            sbom=None,
            quality_gate=row["status_qualitygate"],
            certificate=None,
        )

    @staticmethod
    def _get_critical_vulnerability_count(audit: Audit) -> int:          
        """Count critical vulnerabilities."""
        count = 0

        for vulnerability in (audit.vulnerabilities or []):
            if isinstance(vulnerability, dict):                               
                severity = vulnerability.get("severity")
            else:
                severity = getattr(vulnerability, "severity", None)

            if severity and str(severity).lower() in (
                "critical", "critique"
            ):
                count += 1

        return count

    @log
    def create(self, audit: Audit) -> bool:
        """Create an audit in the database."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO audit_table (
                            id_project,
                            date,
                            total_vulnerability,
                            total_critical_vulnerability,
                            complexity,
                            energy_comsumption,
                            carbon_emission_gco2e,
                            status_qualitygate
                        )
                        VALUES (
                            %(id_project)s,
                            COALESCE(%(date)s, CURRENT_TIMESTAMP),
                            %(total_vulnerability)s,
                            %(total_critical_vulnerability)s,
                            %(complexity)s,
                            %(energy_comsumption)s,
                            %(carbon_emission_gco2e)s,
                            %(status_qualitygate)s
                        )
                        RETURNING id_audit, date;
                        """,
                        {
                            "id_project": audit.id_project,
                            "date": audit.date,
                            "total_vulnerability": len(
                                audit.vulnerabilities or []
                            ),
                            "total_critical_vulnerability":
                                self._get_critical_vulnerability_count(audit),
                            "complexity": audit.complexity,
                            "energy_comsumption":
                                audit.energy_consumption_kwh,
                            "carbon_emission_gco2e":
                                audit.carbon_emission_gco2e,
                            "status_qualitygate": (
                                audit.quality_gate
                                if isinstance(audit.quality_gate, str)
                                else getattr(
                                    audit.quality_gate, "status", None
                                )
                            ),
                        },
                    )
                    res = cursor.fetchone()

            if res:
                audit.id_audit = res["id_audit"]
                audit.date = res["date"]
                return True

            return False

        except Exception as e:
            logger.error(e)
            raise

    @log
    def find_by_id(self, id_audit: int) -> Audit:
        """Find an audit by its ID."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM audit_table
                        WHERE id_audit = %(id_audit)s;
                        """,
                        {"id_audit": id_audit},
                    )
                    res = cursor.fetchone()

            if res:
                return self._row_to_audit(res)

            return None

        except Exception as e:
            logger.error(e)
            raise

    @log
    def find_all(self) -> list[Audit]:
        """Return all audits ordered by ID."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM audit_table
                        ORDER BY id_audit;
                        """
                    )
                    rows = cursor.fetchall()

            return [self._row_to_audit(row) for row in rows]

        except Exception as e:
            logger.error(e)
            raise

    @log
    def update(self, audit: Audit) -> bool:
        """Update an existing audit."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE audit_table
                        SET id_project = %(id_project)s,
                            date = %(date)s,
                            total_vulnerability = %(total_vulnerability)s,
                            total_critical_vulnerability =
                                %(total_critical_vulnerability)s,
                            complexity = %(complexity)s,
                            energy_comsumption = %(energy_comsumption)s,
                            carbon_emission_gco2e =
                                %(carbon_emission_gco2e)s,
                            status_qualitygate = %(status_qualitygate)s
                        WHERE id_audit = %(id_audit)s;
                        """,
                        {
                            "id_audit": audit.id_audit,
                            "id_project": audit.id_project,
                            "date": audit.date,
                            "total_vulnerability": len(
                                audit.vulnerabilities or []
                            ),
                            "total_critical_vulnerability":
                                self._get_critical_vulnerability_count(audit),
                            "complexity": audit.complexity,
                            "energy_comsumption":
                                audit.energy_consumption_kwh,
                            "carbon_emission_gco2e":
                                audit.carbon_emission_gco2e,
                            "status_qualitygate": (
                                audit.quality_gate
                                if isinstance(audit.quality_gate, str)
                                else getattr(
                                    audit.quality_gate, "status", None
                                )
                            ),
                        },
                    )
                    return cursor.rowcount == 1

        except Exception as e:
            logger.error(e)
            raise

    @log
    def delete(self, audit: Audit) -> bool:
        """Delete an audit from the database."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM audit_table
                        WHERE id_audit = %(id_audit)s;
                        """,
                        {"id_audit": audit.id_audit},
                    )
                    return cursor.rowcount > 0

        except Exception as e:
            logger.error(e)
            raise
