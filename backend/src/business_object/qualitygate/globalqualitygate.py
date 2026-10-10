from business_object.audit import Audit
from business_object.qualitygate.qualitygate import QualityGate
from business_object.vulnerability.critical_vulnerability import CriticalVulnerability


class GlobalQualityGate(QualityGate):
    """
    Class representing the global quality gate expected for an audit of a project
    Attributes:
        max_vulnerabilities (int): Max vulnerabilities tolerated for a project
        max_critical_vulnerabilities (int): Max critical vulnerabilities tolerated for a project
        max_carbon_emission (int): Max carbon emission tolerated for a project
        max_energy_consumption (int) : Max energy consumption tolerated for a project
        status (str): Status of the quality gate
    """

    def __init__(
        self,
        max_vulnerabilities,
        max_critical_vulnerabilities,
        max_carbon_emission,
        max_energy_consumption,
        status,
    ):
        """Constructor"""
        self.max_vulnerabilities = max_vulnerabilities
        self.max_critical_vulnerabilities = max_critical_vulnerabilities
        self.max_carbon_emission = max_carbon_emission
        self.max_energy_consumption = max_energy_consumption
        self.status = status

    def __str__(self) -> str:
        """Returns a string representation of the quality gate.
        Returns:
            str: A string containing the status and the details of the quality gate.
        """
        return (
            f"Status : {self.status}"
            + "\n"
            + f"Details : {self.max_vulnerabilities} max vulnerabilities, {self.max_critical_vulnerabilities} max critical vulnerabilities, {self.max_carbon_emission} max carbon emission, {self.max_energy_consumption} max energy consumption"
        )

    def evaluate(self, audit: Audit) -> bool:
        """Evaluate the Audit
        Args:
            audit: The audit to evaluate

        Returns
            boolean object: True if the qualitygate is respected, False otherwise
        """

        # Count of vulnerabilities of audit
        audit_vul = len(audit.vulnerabilities)

        # Count of critical vulnerabilities of audit
        audit_crit_vul = 0
        for vul in audit.max_vulnerabilities:
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
        Récupère le type du qualitygate (ici global)
        """
        return "global"
