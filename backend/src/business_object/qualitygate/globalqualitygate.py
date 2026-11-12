from business_object.audit import Audit
from business_object.qualitygate.qualitygate import QualityGate
from business_object.vulnerability.critical_vulnerability import CriticalVulnerability


class GlobalQualityGate(QualityGate):
    """
    Class representing the global quality gate expected for the audit of a project.

    Attributes
    ----------
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
    """

    def __init__(
        self,
        max_vulnerabilities,
        max_critical_vulnerabilities,
        max_carbon_emission,
        max_energy_consumption,
        status,
    ) -> None:
        """Constructor"""
        self.max_vulnerabilities = max_vulnerabilities
        self.max_critical_vulnerabilities = max_critical_vulnerabilities
        self.max_carbon_emission = max_carbon_emission
        self.max_energy_consumption = max_energy_consumption
        self.status = status

    def __str__(self) -> str:
        """
        Return a string representation of the quality gate.

        Returns
        -------
        str
            String containing the status and the details of the quality gate.
        """
        return (
            f"Status : {self.status}"
            + "\n"
            + f"Details : {self.max_vulnerabilities} max vulnerabilities, {self.max_critical_vulnerabilities} max critical vulnerabilities, {self.max_carbon_emission} max carbon emission, {self.max_energy_consumption} max energy consumption"
        )

    def evaluate(self, audit: Audit) -> bool:
        """
        Evaluate the audit against the quality gate.

        Checks the results of the audit against the thresholds defined
        by the quality gate.

        Parameters
        ----------
        audit : Audit
            Audit to evaluate.

        Returns
        -------
        bool
            True if the quality gate is respected, False otherwise.
        """

        # Count of vulnerabilities of audit
        audit_vul = len(audit.vulnerabilities)

        # Count of critical vulnerabilities of audit
        audit_crit_vul = 0
        for vul in audit.vulnerabilities:
            if isinstance(vul, CriticalVulnerability):
                audit_crit_vul += 1

        conditions = (
            (audit_vul <= self.max_vulnerabilities)
            & (audit_crit_vul <= self.max_critical_vulnerabilities)
            & (audit.carbon_emission_gco2e <= self.max_carbon_emission)
            & (audit.energy_consumption_kwh <= self.max_energy_consumption)
        )

        return conditions

    def get_type(self) -> str:
        """
        Return the type of the quality gate.

        Returns
        -------
        str
            Type of the quality gate, always ``'global'`` for this class.
        """
        return "global"
