from business_object.audit import Audit

# from business_object.certificate import Certificate
from business_object.qualitygate.qualitygate import QualityGate
from service.qualitygate_services.ecoqualitygate_service import EcoQualityGateService
from service.qualitygate_services.globalqualitygate_service import GlobalQualityGateService
from service.qualitygate_services.securityqualitygate_service import SecurityQualityGateService
from utils.log_utils import log


class QualityGateService:
    """
    Service that handles business logic related to a qualitygate
    """

    @log
    def create(
        self, type_qualitygate: str,
        max_vulnerabilities: int,
        max_critical_vulnerabilities: int,
        max_carbon_emission: float,
        max_energy_consumption: float) -> QualityGate | None:
        """Create a QualityGate object of the type chosen
        Args:
            type_qualitygate (str): type of the qualitygate
            *args (tuple): arguments needed for the qualitygate chosen
        Return:
            Return a QualityGate if the"""
        if type_qualitygate == "global":
            GlobalQualityGateService.create(max_vulnerabilities, max_critical_vulnerabilities, max_carbon_emission, max_energy_consumption)
        if type_qualitygate == "eco":
            EcoQualityGateService.create(max_carbon_emission, max_energy_consumption)
        if type_qualitygate == "security":
            SecurityQualityGateService.create(max_vulnerabilities, max_critical_vulnerabilities)
        else:
            return None

    @log
    def evaluate(self, qualitygate: QualityGate, audit: Audit):
        """Evaluate a project during its audit with the qualitygate chosen
        Args:
            qualitygate (QualityGate) : the qualitygate chosen for the evaluation
            audit (Audit) : the audit of the project that is evaluate
        """
        audit.quality_gate = qualitygate
        if qualitygate.evaluate(audit):
            audit.quality_gate.status = "Passed"
        else:
            audit.quality_gate.status = "Failed"
