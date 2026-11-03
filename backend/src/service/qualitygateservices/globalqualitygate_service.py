from business_object.qualitygate.globalqualitygate import GlobalQualityGate
from utils.log_utils import log


class GlobalQualityGateService:
    """
    Service that handles business logic related to a globalqualitygateservice
    """
    @log
    def create(self, max_vulnerabilities: int, max_critical_vulnerabilities: int, max_carbon_emission: int, max_energy_consumption: int, *args) -> GlobalQualityGate:
        """ Create a GlobalQualityGate object
        Args:
            max_vulnerabilities (int): threehold of vulnerabilities
            max_critical_vulnerabilities (int): threehold of critical vulnerabilities
            max_carbon_emission (int): threehold of carbon emission
            max_energy_consumption (int): threehold of energy consumption
        Return:
            Return an GlobalQualityGate object
        """
        return GlobalQualityGate(max_vulnerabilities, max_critical_vulnerabilities, max_carbon_emission, max_energy_consumption)
