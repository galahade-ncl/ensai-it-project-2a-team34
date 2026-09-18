class QualityGate:
    """
    Class representing the quality gate expected for an audit of a project
    Attributes:
        id_qualitygate (int): The unique identifier of the quality gate
        max_vulnerabilities (int): Total of vulnerabilities of the project
        max_critical_vulnerabilities (int): Total of citical vulnerabilities of the project
        max_carbon_emission (int): Total of carbon emission of the project
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
        return f"Status : {self.status}" + "\n" + f"Details : {self.max_vulnerabilities}) vulnerabilities, {self.max_critical_vulnerabilities} critical vulnerabilities, {self.max_carbon_emission} carbon emission"
