from business_object.audit import Audit


class ServiceQualityGate:
    def __init__(self, id_quality_gate, max_vulnerabilities, max_critical_vulnerabilities, status):
        self.id_quality_gate = id_quality_gate
        self.max_vulnerabilities = max_vulnerabilities
        self.max_critical_vulnerabilities = max_critical_vulnerabilities
        self.status = status

    def evaluate(self, audit : Audit):
        if len(audit.vulnerabilities) > self.max_vulnerabilities:
            return ("The number of vulnerabilities is too high")
            
