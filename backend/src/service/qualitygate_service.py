from business_object.audit import Audit
from business_object.certificate import Certificate
from business_object.qualitygate.qualitygate import QualityGate
from utils.log_utils import log


class QualityGateService:
    """
    Service that handles business logic related to a qualitygate
    """

    @log
    def evaluate(self, qualitygate: QualityGate, audit: Audit) -> bool:
        """Evaluate a project during its audit with the qualitygate chosen
        Args:
            qualitygate (QualityGate) : the qualitygate chosen for the evaluation
            audit (Audit) : the audit of the project that is evaluate
        Returns:
            Boolean object: True if the qualitygate is respected, False otherwise
        """
        audit.quality_gate = qualitygate
        return qualitygate.evaluate(audit)

    @log
    def generate_certificate(self, audit: Audit) -> Certificate:
        """Generate a certificate for a project during its audit
        Args:
            audit (Audit) : the audit of the project
        Returns:
            Certificate object linked to the project
        """
        return Certificate(
            # il nous faut une table Certificate, ou alors on attribut l'id de l'audit au certificat
            id_certificate=audit.id_audit,
            date=audit.date,
            type=audit.quality_gate.get_type(),
            status=audit.quality_gate.status,
            # utilité de path ? path=
        )
