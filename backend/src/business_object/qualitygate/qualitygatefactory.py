from business_object.qualitygate.ecoqualitygate import EcoQualityGate
from business_object.qualitygate.globalqualitygate import GlobalQualityGate
from business_object.qualitygate.qualitygate import QualityGate
from business_object.qualitygate.securityqualitygate import SecurityQualityGate


class QualityGateFactory:
    """
    Factory class to create the appropriate QualityGate instances
    based on a string identifier.

    Methods
    -------
    get_qualitygate(type)
        Return an instance of the QualityGate matching the requested type.
    """

    @staticmethod
    def get_qualitygate(type_qualitygate: str,
        max_vulnerabilities: int,
        max_critical_vulnerabilities: int,
        max_carbon_emission: float,
        max_energy_consumption: float,
        status: str) -> QualityGate:
        """
        Return an instance of the requested type of quality gate.

        Parameters
        ----------
        type_qualitygate : str
            Type of the quality gate expected (``'eco'``, ``'security'``
            or ``'global'``). The value is case-insensitive.
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
            Instance of a class implementing QualityGate.

        Raises
        ------
        ValueError
            If the requested type is not supported.
        """
        type_qg = type_qualitygate.lower()

        if type_qg == "eco":
            return EcoQualityGate(max_carbon_emission, max_energy_consumption, status)
        if type_qg == "security":
            return SecurityQualityGate(max_vulnerabilities, max_critical_vulnerabilities, status)
        if type_qg == "global":
            return GlobalQualityGate(
                max_vulnerabilities,
                max_critical_vulnerabilities,
                max_carbon_emission,
                max_energy_consumption,
                status,
            )
        raise ValueError(f"'{type_qualitygate}' QualityGate is not supported.")
