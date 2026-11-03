from service.qualitygateservices.ecoqualitygate_service import EcoQualityGateService
from service.qualitygateservices.globalqualitygate_service import GlobalQualityGateService
from service.qualitygateservices.securityqualitygate_service import SecurityQualityGateService

from business_object.audit import Audit

# from business_object.certificate import Certificate
from business_object.qualitygate.qualitygate import QualityGate
from utils.log_utils import log


class QualityGateService:
    """
    Service that handles business logic related to a qualitygate
    """

    @log
    def create(self, type_qualitygate: str, *args) -> QualityGate | None:
        """ Create a QualityGate object of the type chosen
        Args:
            type_qualitygate (str): type of the qualitygate
            *args (tuple): arguments needed for the qualitygate chosen
        Return:
            Return a QualityGate if the """
        if type_qualitygate == "global":
            GlobalQualityGateService.create(*args)
        if type_qualitygate == "eco":
            EcoQualityGateService.create(*args)
        if type_qualitygate == "security":
            SecurityQualityGateService.create(*args)
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
