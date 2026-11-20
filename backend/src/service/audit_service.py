from datetime import datetime

from business_object.antipattern.antipattern import AntiPattern
from business_object.audit import Audit
from business_object.file.certificatefile import CertificateFile
from business_object.file.sbomfile import SBOMFile
from business_object.licence import Licence
from business_object.project import Project
from business_object.qualitygate.qualitygate import QualityGate
from business_object.vulnerability.vulnerability import Vulnerability
from dao.audit_dao import AuditDao
from service.certificate_service import CertificateService
from service.eco_service import EcoService
from service.qualitygate_service import QualityGateService
from service.sbom_service import SBOMService
from service.security_service import SecurityService
from utils.log_utils import log


class AuditService:
    """
    Service that handles business logic related to the audit of a project.

    Methods
    -------
    create(...)
        Create a new audit and store it.
    find_by_id(id_audit)
        Find an audit by its identifier.
    list_all_audit(id_project)
        List all the audits.
    update(audit)
        Update an audit.
    run_audit(project, quality_gate_type)
        Run a full audit on a project.
    """

    @log
    def create(
        self,
        id_project: int,
        date: datetime,
        vulnerabilities: list[Vulnerability],
        licenses: list[Licence],
        anti_patterns: list[AntiPattern],
        complexity: float,
        energy_consumption_kwh: float,
        carbon_emission_gco2e: float,
        sbom: SBOMFile,
        quality_gate: QualityGate,
        certificate: CertificateFile,
    ) -> Audit:
        """
        Create a new audit in the system.

        Parameters
        ----------
        id_project : int
            Unique identifier of the project linked to this audit.
        date : datetime
            Date the audit was created.
        vulnerabilities : list of Vulnerability
            Vulnerabilities found in the dependencies of the project.
        licenses : list of Licence
            Licences used by the dependencies of the project.
        anti_patterns : list of AntiPattern
            Antipatterns found in the project.
        complexity : float
            Complexity of the code.
        energy_consumption_kwh : float
            Energy consumption of the code (kWh).
        carbon_emission_gco2e : float
            Carbon emission of the code (gCO2e).
        sbom : SBOMFile
            Software Bill of Materials, the inventory of components used
            by the project.
        quality_gate : QualityGate
            Quality gate associated with the project.
        certificate : CertificateFile or None
            Certificate associated with the audit.

        Returns
        -------
        Audit or None
            The created audit, or None if the creation failed.
        """
        new_audit = Audit(
            id_project=id_project,
            date=date,
            vulnerabilities=vulnerabilities,
            licenses=licenses,
            anti_patterns=anti_patterns,
            complexity=complexity,
            energy_consumption_kwh=energy_consumption_kwh,
            carbon_emission_gco2e=carbon_emission_gco2e,
            sbom=sbom,
            quality_gate=quality_gate,
            certificate=certificate,
        )
        return new_audit if AuditDao().create(new_audit) else None

    @log
    def find_by_id(self, id_audit: int) -> Audit:
        """
        Find an audit by its identifier.

        Parameters
        ----------
        id_audit : int
            Identifier of the audit.

        Returns
        -------
        Audit or None
            The audit found, or None if the search failed.
        """
        return AuditDao().find_by_id(id_audit)

    @log
    def list_all_audit(self, id_project: int) -> list[Audit]:
        """
        List all the audits of a project.

        Parameters
        ----------
        id_project : int
            Identifier of the project.

        Returns
        -------
        list of Audit
            Audits of the project.
        """
        return AuditDao().find_all(id_project)

    @log
    def update(self, audit: Audit):
        """
        Update an audit.

        Parameters
        ----------
        audit : Audit
            Audit to update.

        Returns
        -------
        bool
            True if the update is successful, False otherwise.
        """
        return AuditDao().update(audit)

    @log
    def run_audit(self, project: Project, quality_gate_type: str):
        """
        Run a full audit on a project.

        Finds the vulnerabilities and licences of the dependencies, analyses
        the code (antipatterns, complexity, energy, carbon), generates the
        SBOM, evaluates the quality gate and, if it is passed, generates
        a certificate.

        Parameters
        ----------
        project : Project
            Project to audit, with its code file and dependency file.
        quality_gate_type : str
            Type of quality gate to apply (``'eco'``, ``'security'`` or
            ``'global'``).

        Returns
        -------
        Audit
            The completed audit.
        """
        id_project = project.id_project

        max_vuln = 5
        max_critical_vuln = 0
        max_carbon = 1
        max_energy = 0.001

        dep_file = project.dependencyfile

        # -----------------
        #  SecurityService
        # -----------------
        vulnerabilities = SecurityService().find_vulnerabilities(dep_file)
        licenses = SecurityService().find_licences(dep_file)

        code_file = project.codefile

        # ------------
        #  EcoService
        # ------------
        analysis = EcoService().analyze(code_file)

        anti_patterns = analysis.antipatterns
        complexity = analysis.complexity
        energy_consumption_kwh = analysis.energy_kwh
        carbon_emission_gco2e = analysis.carbon_gco2e

        sbom = SBOMService().generate(project, vulnerabilities)

        quality_gate = QualityGateService().create(
            quality_gate_type,
            max_vulnerabilities=max_vuln,
            max_critical_vulnerabilities=max_critical_vuln,
            max_carbon_emission=max_carbon,
            max_energy_consumption=max_energy,
            status="Unevaluated",
        )

        date = datetime.now()

        audit = AuditService().create(
            id_project,
            date,
            vulnerabilities,
            licenses,
            anti_patterns,
            complexity,
            energy_consumption_kwh,
            carbon_emission_gco2e,
            sbom,
            quality_gate,
            None,
        )

        # Stop if the audit could not be persisted.
        if audit is None:
            return None

        # Evaluate the audit
        QualityGateService().evaluate(quality_gate, audit)

        # Generate a Certificate if needed
        if audit.quality_gate.status == "Passed":
            audit.certificate = CertificateService().generate_certificate(
                audit, project, quality_gate_type
            )

        AuditService().update(audit)

        return audit
