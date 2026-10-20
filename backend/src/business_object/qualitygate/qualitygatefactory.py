from business_object.qualitygate.servicequalitygate import SecurityQualityGate

from business_object.qualitygate.ecoqualitygate import EcoQualityGate
from business_object.qualitygate.globalqualitygate import GlobalQualityGate
from business_object.qualitygate.qualitygate import QualityGate


class QualityGateFactory:
    """
    Factory class to create appropriate QualityGate instances
    based on a string identifier.
    """

    @classmethod
    def get_qualitygate(self, type: str) -> QualityGate:
        """
        Returns the type of QualityGate asked.
        Args:
            type (str): The type of the QualityGate expected (e.g., 'eco', 'service', 'global').
        Returns:
            QualityGate: An instance of a class implementing QualityGate.
        Raises:
            ValueError: If the requested type is not supported.
        """
        type = type.lower()

        if type == "eco":
            return EcoQualityGate()
        elif type == "security":
            return SecurityQualityGate()
        elif type == "security":
            return GlobalQualityGate()
        else:
            raise ValueError(f"'{type}'QualityGate is not supported.")
