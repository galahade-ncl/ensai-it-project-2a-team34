import json

from business_object.audit import Audit
from business_object.file.certificatefile import CertificateFile
from business_object.project import Project
from dao.db_connection import DBConnection
from service.qualitygate_services.qualitygate_service import QualityGateService
from service.sbom_service import SBOMService
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class AuditDao(metaclass=Singleton):
    """Class containing methods to access Audits in the database."""

    @staticmethod
    def _row_to_audit(row: dict) -> Audit:
        """Convert a database row into an Audit object."""
        signed = row.get("certificate_signed")
        if isinstance(signed, str):  # selon le driver, JSONB peut arriver en str
            signed = json.loads(signed)

        if signed and row.get("certificate_pdf"):
            certificate = CertificateFile(
                name="Certificate: " + row["type_qualitygate"],
                content=bytes(row["certificate_pdf"]),  # bytes() gère memoryview
                type_file="pdf",
                qualitygate_type=row["type_qualitygate"],
                date=signed["payload"]["issued_at"][:10],
                signed_data=signed,
            )
        else:
            certificate = None
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
            sbom=SBOMService().create_empty_sbom(),
            quality_gate=QualityGateService().create(
                row["type_qualitygate"], 5, 0, 1, 0.001, row["status_qualitygate"]
            ),
            certificate=certificate,
        )

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
                            complexity,
                            energy_comsumption,
                            carbon_emission_gco2e,
                            type_qualitygate,
                            status_qualitygate
                        )
                        VALUES (
                            %(id_project)s,
                            COALESCE(%(date)s, CURRENT_TIMESTAMP),
                            %(complexity)s,
                            %(energy_comsumption)s,
                            %(carbon_emission_gco2e)s,
                            %(type_qualitygate)s,
                            %(status_qualitygate)s
                        )
                        RETURNING id_audit, date;
                        """,
                        {
                            "id_project": audit.id_project,
                            "date": audit.date,
                            "complexity": audit.complexity,
                            "energy_comsumption": audit.energy_consumption_kwh,
                            "carbon_emission_gco2e": audit.carbon_emission_gco2e,
                            "type_qualitygate": audit.quality_gate.get_type(),
                            "status_qualitygate": (
                                audit.quality_gate
                                if isinstance(audit.quality_gate, str)
                                else getattr(audit.quality_gate, "status", None)
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
                    cursor.execute("""
                        SELECT *
                        FROM audit_table
                        ORDER BY id_audit;
                        """)
                    rows = cursor.fetchall()

            return [self._row_to_audit(row) for row in rows]

        except Exception as e:
            logger.error(e)
            raise

    @log
    def update(self, audit: Audit) -> bool:
        """Update an existing audit."""
        try:
            signed = getattr(audit.certificate, "signed_data", None)

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE audit_table
                        SET id_project = %(id_project)s,
                        date = %(date)s,
                        complexity = %(complexity)s,
                        energy_comsumption = %(energy_comsumption)s,
                        carbon_emission_gco2e = %(carbon_emission_gco2e)s,
                        type_qualitygate = %(type_qualitygate)s,
                        status_qualitygate = %(status_qualitygate)s,
                        certificate_pdf = %(certificate_pdf)s,
                        certificate_signed = %(certificate_signed)s,
                        certificate_id = %(certificate_id)s
                    WHERE id_audit = %(id_audit)s;
                    """,
                        {
                            "id_audit": audit.id_audit,
                            "id_project": audit.id_project,
                            "date": audit.date,
                            "complexity": audit.complexity,
                            "energy_comsumption": audit.energy_consumption_kwh,
                            "carbon_emission_gco2e": audit.carbon_emission_gco2e,
                            "type_qualitygate": audit.quality_gate.get_type(),
                            "status_qualitygate": (
                                audit.quality_gate
                                if isinstance(audit.quality_gate, str)
                                else getattr(audit.quality_gate, "status", None)
                            ),
                            "certificate_pdf": audit.certificate.content if signed else None,
                            "certificate_signed": json.dumps(signed) if signed else None,
                            "certificate_id": signed["payload"]["cert_id"] if signed else None,
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

    @log
    def list_all_audit(self, project: Project) -> list[Audit]:
        """
        List all audits on a given project.

        Arguments
        ---------
        project : Project
            Project whose audits are to be listed

        Returns
        -------
        list[Audit]
            List of the project's audits, or an empty list if there are none
        """
        res = []

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * "
                        "  FROM audit_table "
                        " WHERE id_project = %(id_project)s "
                        " ORDER BY id_audit;",
                        {"id_project": project.id_project},
                    )
                    res = cursor.fetchall()
            return [self._row_to_audit(row) for row in res]

        except Exception as e:
            logger.error(e)
            raise
