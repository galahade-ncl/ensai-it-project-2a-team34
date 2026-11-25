import json

from business_object.audit import Audit
from business_object.file.certificatefile import CertificateFile
from business_object.file.sbomfile import SBOMFile
from business_object.project import Project
from dao.db_connection import DBConnection
from service.qualitygate_service import QualityGateService
from service.sbom_service import SBOMService
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class AuditDao(metaclass=Singleton):
    """
    Class containing methods to access Audits in the database.

    Methods
    -------
    _row_to_audit(row)
        Convert a database row into an Audit object.
    create(audit)
        Create an audit in the database.
    find_by_id(id_audit)
        Find an audit by its identifier.
    find_all()
        Retrieve all audits from the database.
    update(audit)
        Update an existing audit in the database.
    delete(audit)
        Delete an audit from the database.
    list_all_audit(project)
        Retrieve all audits associated with a project.
    """

    @staticmethod
    def _get_quality_gate_data(quality_gate):
        if quality_gate is None:
            return None, None

        if isinstance(quality_gate, str):
            # Compatibilité avec les anciens tests
            return None, quality_gate

        return (
            quality_gate.get_type(),
            getattr(quality_gate, "status", None),
        )

    @staticmethod
    def _row_to_audit(row: dict) -> Audit:
        """
        Convert a database row into an Audit object.

        This method reconstructs an Audit instance from a database row.
        It also reconstructs the associated certificate and SBOM when
        available. If no SBOM is stored, an empty SBOM is created.

        Parameters
        ----------
        row : dict
            Database row containing the audit information, including
            its identifiers, date, quality gate, metrics, SBOM content
            and optional certificate information.

        Returns
        -------
        Audit
            Audit object reconstructed from the database row.
            The certificate is set to None if no signed certificate
            and PDF content are available.
        """
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
        if row.get("sbom_content"):
            sbom = SBOMFile(
                name=f"sbom_{row['id_audit']}.json",
                content=bytes(row["sbom_content"]),
                type_file="json",
                date=row["date"],
            )
        else:
            sbom = SBOMService().create_empty_sbom()
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
            sbom=sbom,
            quality_gate=QualityGateService().create(
                row["type_qualitygate"], 5, 0, 1, 0.001, row["status_qualitygate"]
            ),
            certificate=certificate,
        )

    @log
    def create(self, audit: Audit) -> bool:
        """
        Create an audit in the database.

        The audit identifier and date generated or assigned by the
        database are set on the provided audit object.

        Parameters
        ----------
        audit : Audit
            Audit to create in the database. Contains the project
            identifier, date, complexity, energy consumption,
            carbon emissions, quality gate and SBOM information.

        Returns
        -------
        bool
            True if the audit is successfully created and its
            identifier is returned by the database, False otherwise.

        Raises
        ------
        Exception
            If an error occurs during database insertion.
        """
        type_qualitygate, status_qualitygate = self._get_quality_gate_data(audit.quality_gate)
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
                            status_qualitygate,
                            sbom_content
                        )
                        VALUES (
                            %(id_project)s,
                            COALESCE(%(date)s, CURRENT_TIMESTAMP),
                            %(complexity)s,
                            %(energy_comsumption)s,
                            %(carbon_emission_gco2e)s,
                            %(type_qualitygate)s,
                            %(status_qualitygate)s,
                            %(sbom_content)s
                        )
                        RETURNING id_audit, date;
                        """,
                        {
                            "id_project": audit.id_project,
                            "date": audit.date,
                            "complexity": audit.complexity,
                            "energy_comsumption": audit.energy_consumption_kwh,
                            "carbon_emission_gco2e": audit.carbon_emission_gco2e,
                            "type_qualitygate": type_qualitygate,
                            "status_qualitygate": status_qualitygate,
                            "sbom_content": getattr(audit.sbom, "content", None),
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
        """
        Find an audit by its identifier.

        Parameters
        ----------
        id_audit : int
            Identifier of the audit to retrieve.

        Returns
        -------
        Audit or None
            Audit object corresponding to the provided identifier,
            or None if no audit is found.

        Raises
        ------
        Exception
            If an error occurs during database retrieval.
        """
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
        """
        Retrieve all audits from the database.

        Audits are ordered by their identifier in ascending order.

        Returns
        -------
        list[Audit]
            List of all audits stored in the database.
            Returns an empty list if no audit is found.

        Raises
        ------
        Exception
            If an error occurs during database retrieval.
        """
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
        """
        Update an existing audit in the database.

        The audit is identified by its identifier. Its project,
        date, complexity, energy consumption, carbon emissions,
        quality gate and certificate information are updated.

        Certificate PDF content and signed data are stored when
        a signed certificate is associated with the audit.

        Parameters
        ----------
        audit : Audit
            Audit containing the updated information.
            The audit identifier is used to identify the database
            record to update.

        Returns
        -------
        bool
            True if exactly one audit is updated, False otherwise.

        Raises
        ------
        Exception
            If an error occurs during database update.
        """
        type_qualitygate, status_qualitygate = self._get_quality_gate_data(audit.quality_gate)
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
                            "type_qualitygate": type_qualitygate,
                            "status_qualitygate": status_qualitygate,
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
        """
        Delete an audit from the database.

        The audit is identified by its identifier.

        Parameters
        ----------
        audit : Audit
            Audit to delete from the database.
            Its identifier is used to locate the corresponding record.

        Returns
        -------
        bool
            True if at least one audit is deleted, False if no
            matching audit is found.

        Raises
        ------
        Exception
            If an error occurs during database deletion.
        """
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
        Retrieve all audits associated with a given project.

        Audits are ordered by their identifier in ascending order.

        Parameters
        ----------
        project : Project
            Project whose audits are to be retrieved.
            Its identifier is used to filter the database records.

        Returns
        -------
        list[Audit]
            List of audits associated with the specified project.
            Returns an empty list if the project has no audits.

        Raises
        ------
        Exception
            If an error occurs during database retrieval.
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
