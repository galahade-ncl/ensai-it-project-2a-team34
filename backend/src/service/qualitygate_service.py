from business_object.audit import Audit
from business_object.qualitygate.qualitygate import QualityGate
from business_object.qualitygate.qualitygatefactory import QualityGateFactory
from utils.log_utils import log


class QualityGateService:
    """
    Service that handles business logic related to a quality gate.
    """

    @log
    def create(
        self,
        type_qualitygate: str,
        max_vulnerabilities: int,
        max_critical_vulnerabilities: int,
        max_carbon_emission: float,
        max_energy_consumption: float,
        status: str,
    ) -> QualityGate:
        """
        Create a QualityGate object of the chosen type.

        Parameters
        ----------
        type_qualitygate : str
            Type of the quality gate (``'eco'``, ``'security'`` or ``'global'``).
        max_vulnerabilities : int
            Maximum number of vulnerabilities tolerated for a project.
        max_critical_vulnerabilities : int
            Maximum number of critical vulnerabilities tolerated for a project.
        max_carbon_emission : float
            Maximum carbon emission tolerated for a project.
        max_energy_consumption : float
            Maximum energy consumption tolerated for a project.
        status : str
            Status of the quality gate.

        Returns
        -------
        QualityGate
            Quality gate of the requested type.

        Raises
        ------
        ValueError
            If the requested type is not supported.
        """
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
        """
        Evaluate the audit of a project with the chosen quality gate.

        The quality gate is attached to the audit and its status is set
        to ``'Passed'`` or ``'Failed'``.

        Parameters
        ----------
        qualitygate : QualityGate
            Quality gate chosen for the evaluation.
        audit : Audit
            Audit of the project to evaluate.

        Returns
        -------
        None
        """
        audit.quality_gate = qualitygate
        if qualitygate.evaluate(audit):
            audit.quality_gate.status = "Passed"
        else:
            audit.quality_gate.status = "Failed"
