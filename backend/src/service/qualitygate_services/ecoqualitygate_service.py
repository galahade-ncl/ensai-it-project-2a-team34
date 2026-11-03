from business_object.qualitygate.ecoqualitygate import EcoQualityGate
from utils.log_utils import log


class EcoQualityGateService:
    """
    Service that handles business logic related to a ecoqualitygate
    """
    @log
    def create(self, max_carbon_emission: int, max_energy_consumption: int, *args) -> EcoQualityGate:
        """ Create a EcoQualityGate object
        Args:
            max_carbon_emission (int): threehold of carbon emission
            max_energy_consumption (int): threehold of energy consumption
        Return:
            Return an EcoQualityGate object
        """
        return EcoQualityGate(max_carbon_emission, max_energy_consumption)
