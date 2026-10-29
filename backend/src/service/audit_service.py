import datetime

from business_object.antipattern.antipattern import AntiPattern
from business_object.audit import Audit
from business_object.certificate import Certificate
from business_object.licence import Licence
from business_object.qualitygate.qualitygate import QualityGate
from business_object.vulnerability.vulnerability import Vulnerability
from dao.audit_dao import AuditDao
from utils.log_utils import log


class AuditService:
    """
    Service that handles business logic related to the eco analyse of a Python code
    """

    @log
    def create(
        self,
        id_audit: int,
        id_project: int,
        date: datetime,
        vulnerabilities: list[Vulnerability],
        licenses: list[Licence],
        anti_patterns: list[AntiPattern],
        complexity: float,
        energy_consumption_kwh: float,
        carbon_emission_gco2e: float,
        quality_gate: QualityGate,
        certificate: list[Certificate]
        ) -> Audit:
        """
        Create a new audit in the system
        Args:
            id_project (int) : The unique identifier of the project from which this audit is linked
            date (datetime) : The date the audit was created
            vulnerabilities (list[Vulnerability]) : The list of vulnerabilities found in the dependancies of the project
            licenses (list[License]) : The list of licence used by the code of the project
            anti_patterns (list[AntiPattern]) : The list of antipatterns found in the project
            complexity (float) : The complexity of the code
            energy_consumption_kwh (float) : The energy consumption of the code (kwh)
            carbon_emission_gco2e (float) : The carbon emission of the code
            quality_gate (QualityGate) : The quality gate associated to the project
            certificate (Certificate) : The certificate associated to the audit
        Returns:
            Audit object created or None if failed
        """
        new_audit = Audit(id_project=id_project, date=date, vulnerabilities=vulnerabilities, licenses=licenses, anti_patterns=anti_patterns, complexity=complexity, energy_consumption_kwh=energy_consumption_kwh, carbon_emission_gco2e=carbon_emission_gco2e, quality_gate=quality_gate, certificate=certificate)
        return new_audit if AuditDao().create(new_audit) else None

    @log
    def find_by_id(self, id_audit: int) -> Audit:
        """
        Find an audit by an its id
        Args:
            id_audit (int) : The id of the audit
        Returns:
            Audit or None if search failed
        """
        return AuditDao().find_by_id(id_audit)

    @log
    def list_all_audit(self, id_project: int) -> list[Audit]:
        """
        List all the audit
        Args:
            id
        Returns:
            The list of audits
        """
        return AuditDao().find_all(id_project)
