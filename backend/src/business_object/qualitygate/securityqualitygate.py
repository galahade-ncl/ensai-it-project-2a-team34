from business_object.audit import Audit


class SecurityQualityGate:
    """
    Class representing the security quality gate expected for the audit of a project.

    Attributes
    ----------
    max_vulnerabilities : int
        Maximum number of vulnerabilities tolerated for a project.
    max_critical_vulnerabilities : int
        Maximum number of critical vulnerabilities tolerated for a project.
    status : str
        Status of the quality gate.

    Methods
    -------
    evaluate(audit)
        Check whether the project stays within the vulnerability threshold.
    get_type()
        Return the type of the quality gate, always ``'security'``.
    """
    def __init__(self, max_vulnerabilities, max_critical_vulnerabilities, status) -> None:
        self.max_vulnerabilities = max_vulnerabilities
        self.max_critical_vulnerabilities = max_critical_vulnerabilities
        self.status = status

    def evaluate(self, audit: Audit) -> bool:
        """
        Check whether the project stays within the vulnerability threshold.

        Compares the number of vulnerabilities found in the audit with the
        maximum number tolerated by the quality gate.

        Parameters
        ----------
        audit : Audit
            Audit of the project.

        Returns
        -------
        bool
            True if the project does not exceed the threshold.
        """
        return len(audit.vulnerabilities) <= self.max_vulnerabilities

    def get_type(self) -> str:
        """
        Return the type of the quality gate.

        Returns
        -------
        str
            Type of the quality gate, always ``'security'`` for this class.
        """
        return "security"
