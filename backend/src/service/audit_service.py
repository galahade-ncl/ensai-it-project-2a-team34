from datetime import datetime

from business_object.antipattern.antipattern import AntiPattern
from business_object.audit import Audit
from business_object.certificate import Certificate
from business_object.licence import Licence
from business_object.project import Project
from business_object.qualitygate.qualitygate import QualityGate
from business_object.vulnerability.vulnerability import Vulnerability
from utils.log_utils import log


class AuditService:
    """Service that handles business logic related to an audit"""

    @log
    def create(
        id_audit: int,
        id_project: int,
        date: datetime,
        vulnerabilities: list[Vulnerability],
        licenses: list[Licence],
        anti_patterns: list[AntiPattern],
        complexity: float,
        sbom,
        energy_consumption_kwh: float,
        carbon_emission_gco2e: float,
        quality_gate: QualityGate,
        certificate: list[Certificate],
    ):
        pass

    def run_audit(project: Project) -> Audit:
        pass
