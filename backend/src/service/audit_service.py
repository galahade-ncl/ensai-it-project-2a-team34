from datetime import datetime

from business_object.audit import Audit
from business_object.project import Project
from business_object.vulnerability.vulnerability import Vulnerability
from dao.audit_dao import AuditDao
from service.eco_service import EcoService
from service.security_service import SecurityService
from utils.log_utils import log


class AuditService:
    """Service that handles business logic related to an audit."""

    @log
    def create(
        self,
        id_audit: int | None,
        id_project: int,
        date: datetime,
        vulnerabilities: list[Vulnerability] | None,
        licenses: list,
        anti_patterns: list,
        complexity: float,
        sbom,
        energy_consumption_kwh: float,
        carbon_emission_gco2e: float,
        quality_gate,
        certificate,
    ) -> Audit | None:
        """Create and persist an audit."""

        audit = Audit(
            id_audit=id_audit,
            id_project=id_project,
            date=date,
            vulnerabilities=vulnerabilities or [],
            licenses=licenses or [],
            anti_patterns=anti_patterns or [],
            complexity=complexity,
            energy_consumption_kwh=energy_consumption_kwh,
            carbon_emission_gco2e=carbon_emission_gco2e,
            sbom=sbom,
            quality_gate=quality_gate,
            certificate=certificate,
        )

        if AuditDao().create(audit):
            return audit

        return None

    @log
    def run_audit(self, project: Project) -> Audit | None:
        """Run a basic security and eco-analysis on a project."""

        if project.codefile is None:
            raise ValueError(
                "The project must contain a code file to run an audit."
            )

        eco_service = EcoService()

        # Analyze the source code.
        metrics = eco_service.analyze_ast(project.codefile)

        # Approximate complexity from the number of conditions and loops.
        complexity = float(
            1 + metrics["conditions"] + metrics["loops"]
        )

        # Estimate energy consumption and carbon emissions.
        energy = eco_service.calculate_energy(project.codefile)
        carbon = eco_service.calculate_carbon(energy)

        # Find vulnerabilities if a dependency file is available.
        vulnerabilities = []

        if project.dependencyfile is not None:
            vulnerabilities = SecurityService().find_vulnerabilities(
                project.dependencyfile
            )

        # The project does not currently specify a quality gate.
        # License analysis, SBOM generation and certificate generation
        # are not implemented here yet.
        return self.create(
            id_audit=None,
            id_project=project.id_project,
            date=datetime.now(),
            vulnerabilities=vulnerabilities,
            licenses=[],
            anti_patterns=[],
            complexity=complexity,
            sbom=None,
            energy_consumption_kwh=energy,
            carbon_emission_gco2e=carbon,
            quality_gate=None,
            certificate=None,
        )
