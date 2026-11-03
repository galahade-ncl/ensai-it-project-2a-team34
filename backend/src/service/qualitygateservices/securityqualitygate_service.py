from business_object.qualitygate.securityqualitygate import SecurityQualityGate
from utils.log_utils import log


class SecurityQualityGateService:
    """
    Service that handles business logic related to a securityqualitygateservice
    """
    @log
    def create(self, max_vulnerabilities: int, max_critical_vulnerabilities: int, *args) -> SecurityQualityGate:
        """ Create a SecurityQualityGate object
        Args:
            max_vulnerabilities (int): threehold of vulnerabilities
            max_critical_vulnerabilities (int): threehold of critical vulnerabilities
        Return:
            Return an SecurityQualityGate object
        """
        return SecurityQualityGate(max_vulnerabilities, max_critical_vulnerabilities)
