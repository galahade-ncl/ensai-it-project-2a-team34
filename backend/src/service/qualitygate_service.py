from business_object.audit import Audit

# from business_object.certificate import Certificate
from business_object.qualitygate.qualitygate import QualityGate
from business_object.qualitygate.qualitygatefactory import QualityGateFactory
from utils.log_utils import log


class QualityGateService:
    """
    Service that handles business logic related to a qualitygate
    """

    """Service that handles business logic related to a qualitygate"""

    @log
    def create(self, type_qualitygate: str, max_vulnerabilities: int,
        max_critical_vulnerabilities: int, max_carbon_emission: float,
        max_energy_consumption: float, status: str) -> QualityGate:
        """Create a QualityGate object of the type chosen
        Args:
            type_qualitygate (str): type of the qualitygate
            *args (tuple): arguments needed for the qualitygate chosen
        Return:
            Return a QualityGate depending of the type of the QualityGate"""
        return QualityGateFactory.get_qualitygate(
            type_qualitygate,
            max_vulnerabilities,
            max_critical_vulnerabilities,
            max_carbon_emission,
            max_energy_consumption,
            status,
        )

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
