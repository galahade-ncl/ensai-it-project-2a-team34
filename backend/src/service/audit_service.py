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
from service.qualitygate_services.qualitygate_service import QualityGateService
from service.sbom_service import SBOMService
from service.security_service import SecurityService
from utils.log_utils import log


class AuditService:
    """
    Service that handles business logic related to the eco analyse of a Python code
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
        Create a new audit in the system
        Args:
            id_audit (int) : The unique identifier of the audit
            id_project (int) : The unique identifier of the project from which this audit is linked
            date (datetime) : The date the audit was created
            vulnerabilities (list[Vulnerability]) : The list of vulnerabilities found in the dependancies of the project
            licenses (list[License]) : The list of licence used by the code of the project
            anti_patterns (list[AntiPattern]) : The list of antipatterns found in the project
            complexity (float) : The complexity of the code
            energy_consumption_kwh (float) : The energy consumption of the code (kwh)
            carbon_emission_gco2e (float) : The carbon emission of the code
            sbom (SBOM): Software Bill of Materials, the inventory of components used for the project
            quality_gate (QualityGate) : The quality gate associated to the project
            certificate (CertificateFile) : The certificate associated to the audit
        Returns:
            Audit object created or None if failed
        """
        new_audit = Audit(id_project=id_project, date=date, vulnerabilities=vulnerabilities, licenses=licenses, anti_patterns=anti_patterns, complexity=complexity, energy_consumption_kwh=energy_consumption_kwh, carbon_emission_gco2e=carbon_emission_gco2e, sbom=sbom, quality_gate=quality_gate, certificate=certificate)
        return new_audit if AuditDao().create(new_audit) else None

    @log
    def find_by_id(self, id_audit: int) -> Audit:
        """
        Find an audit by an its id
        Args:
            id_audit (int) : The id of the audit
        Returns:
            Audit or None if search failed
        """
        return AuditDao().find_by_id(id_audit)

    @log
    def list_all_audit(self, id_project: int) -> list[Audit]:
        """
        List all the audit
        Args:
            id
        Returns:
            The list of audits
        """
        return AuditDao().find_all(id_project)

    @log
    def update(self, audit: Audit):
        """
        Update an Audit
        Args:
            audit
        """
        return AuditDao().update(audit)

    @log
    def run_audit(self, project: Project, quality_gate_type: str):
        """
        Runs an audit on a project
        Args:
            project
        Returns:
            The audit
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

        sbom = SBOMService().generate(project)

        quality_gate = QualityGateService().create(
            quality_gate_type,
            max_vulnerabilities=max_vuln,
            max_critical_vulnerabilities=max_critical_vuln,
            max_carbon_emission=max_carbon,
            max_energy_consumption=max_energy,
            status="Unevaluated"
        )

        certificate = CertificateService().create_empty_certificate()

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
            certificate,
        )

        QualityGateService().evaluate(quality_gate, audit)

        certificate = CertificateService().generate_certificate(audit, project, quality_gate_type)
        audit.certificate = certificate

        # Update qualitygate status in database

        AuditService().update(audit)

        return audit
