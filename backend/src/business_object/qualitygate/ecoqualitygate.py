from business_object.audit import Audit


class EcoQualityGate:
    """
    Class representing the security quality gate (via vulnerabilities) expected for an audit of a project
    Attributes:
        id_quality_gate (int): identifiant of the quality gate
        max_carbon_emission (int): Max carbon emission tolerated for a project
        max_energy_consumption (int) : Max energy consumption tolerated for a project
        status (str): Status of the quality gate
    """
    def __init__(self, id_quality_gate, max_carbon_emission, max_energy_consumption, status):
        self.id_quality_gate = id_quality_gate
        self.max_carbon_emission = max_carbon_emission
        self.max_energy_consumption = max_energy_consumption
        self.status = status

    def evaluate(self, audit : Audit) -> bool:
        """Returns if the project exceed the permissible ecologic threshold
        Parameters:
            audit: The audit of the project

        Returns
            bool: True if the project does not exceed the threshold

        """
        if (audit.carbon_emission_gco2e > self.max_carbon_emission) or (audit.energy_consumption_kwh > self.max_energy_consumption):
            return False

        else:
            return True
