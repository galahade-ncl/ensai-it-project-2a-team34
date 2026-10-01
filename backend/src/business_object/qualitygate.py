class QualityGate:
    """
    Class representing the quality gate expected for an audit of a project
    Attributes:
        id_qualitygate (int): The unique identifier of the quality gate
        max_vulnerabilities (int): Max vulnerabilities tolerated for a project
        max_critical_vulnerabilities (int): Max critical vulnerabilities tolerated for a project
        max_carbon_emission (int): Max carbon emission tolerated for a project
        status (str): Status of the quality gate
    """

    def __init__(
        self,
        max_vulnerabilities,
        max_critical_vulnerabilities,
        max_carbon_emission,
        status,
        id_qualitygate=None,
    ):
        """Constructor"""
        self.id_qualitygate = id_qualitygate
        self.max_vulnerabilities = max_vulnerabilities
        self.max_critical_vulnerabilities = max_critical_vulnerabilities
        self.max_carbon_emission = max_carbon_emission
        self.status = status

    def __str__(self):
        """Returns a string representation of the quality gate.
        Returns:
            str: A string containing the status and the details of the quality gate.
        """
        return f"Status : {self.status}" + "\n" + f"Details : {self.max_vulnerabilities} max vulnerabilities, {self.max_critical_vulnerabilities} max critical vulnerabilities, {self.max_carbon_emission} max carbon emission"
