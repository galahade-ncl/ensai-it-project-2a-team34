from business_object.audit import Audit


class EcoQualityGate:
    """
    Class representing the eco quality gate expected for the audit of a project.

    Attributes
    ----------
    max_carbon_emission : float
        Maximum carbon emission tolerated for a project.
    max_energy_consumption : float
        Maximum energy consumption tolerated for a project.
    status : str
        Status of the quality gate.
    """

    def __init__(self, max_carbon_emission, max_energy_consumption, status) -> None:
        self.max_carbon_emission = max_carbon_emission
        self.max_energy_consumption = max_energy_consumption
        self.status = status

    def evaluate(self, audit: Audit) -> bool:
        """
        Check whether the project stays within the ecological thresholds.

        Compares the carbon emission and the energy consumption of the
        audit with the maximum values tolerated by the quality gate.

        Parameters
        ----------
        audit : Audit
            Audit of the project.

        Returns
        -------
        bool
            True if the project does not exceed the thresholds.
        """
        return (audit.carbon_emission_gco2e <= self.max_carbon_emission) & (
            audit.energy_consumption_kwh <= self.max_energy_consumption
        )

    def get_type(self) -> str:
        """
        Return the type of the quality gate.

        Returns
        -------
        str
            Type of the quality gate, always ``'eco'`` for this class.
        """
        return "eco"
