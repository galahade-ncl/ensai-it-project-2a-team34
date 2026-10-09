from business_object.audit import Audit


class SecurityQualityGate:
    """
    Class representing the security quality gate (via vulnerabilities) expected for an audit of a project
    Attributes:
        id_quality_gate (int): identifiant of the quality gate
        max_vulnerabilities (int): Max vulnerabilities tolerated for a project
        max_critical_vulnerabilities (int): Max critical vulnerabilities tolerated for a project
        status (str): Status of the quality gate
    """

    def __init__(self, id_quality_gate, max_vulnerabilities, max_critical_vulnerabilities, status):
        self.id_quality_gate = id_quality_gate
        self.max_vulnerabilities = max_vulnerabilities
        self.max_critical_vulnerabilities = max_critical_vulnerabilities
        self.status = status

    def evaluate(self, audit: Audit):
        """Returns if the project exceed the permissible vulnerability threshold
        Parameters:
            audit: The audit of the project

        Returns
            bool: True if the project does not exceed the threshold

        """
        return len(audit.vulnerabilities) <= self.max_vulnerabilities

    def get_type(self) -> str:
        """
        Récupère le type du qualitygate (ici security)
        """
        return "security"
