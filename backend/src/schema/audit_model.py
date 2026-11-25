from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from schema.antipattern_model import AntiPatternModel
from schema.certificate_model import CertificateModel
from schema.licence_model import LicenceModel
from schema.project_model import ProjectCompletedModel
from schema.qualitygate_model import QualityGateModel
from schema.vulnerability_model import VulnerabilityModel


# When the user wants information on a past audit
class AuditReadModel(BaseModel):
    """
    Model returned when the user consults a past audit.

    Attributes
    ----------
    id_audit : int
        Unique identifier of the audit.
    id_project : int
        Unique identifier of the audited project.
    date : datetime
        Date of the audit.
    complexity : float
        Complexity of the code.
    energy_consumption_kwh : float
        Energy consumption of the code (kWh).
    carbon_emission_gco2e : float
        Carbon emission of the code (gCO2e).
    quality_gate : QualityGateModel
        Quality gate of the audit.
    """

    id_audit: int
    id_project: int
    date: datetime
    complexity: float
    energy_consumption_kwh: float
    carbon_emission_gco2e: float
    quality_gate: QualityGateModel


# When user runs an audit on a project
class AuditResponseModel(BaseModel):
    """
    Model returned when the user runs an audit on a project.

    Attributes
    ----------
    id_audit : int
        Unique identifier of the audit.
    id_project : int
        Unique identifier of the audited project.
    date : datetime
        Date of the audit.
    vulnerabilities : list of VulnerabilityModel
        Vulnerabilities found in the dependencies.
    licenses : list of LicenceModel or str
        Licences used by the dependencies.
    anti_patterns : list of AntiPatternModel
        Antipatterns found in the code.
    complexity : float
        Complexity of the code.
    energy_consumption_kwh : float
        Energy consumption of the code (kWh).
    carbon_emission_gco2e : float
        Carbon emission of the code (gCO2e).
    quality_gate : QualityGateModel
        Quality gate of the audit.
    certificate : CertificateModel or None
        Certificate issued if the quality gate is respected.
    """

    id_audit: int
    id_project: int
    date: datetime
    vulnerabilities: list[VulnerabilityModel]
    licenses: list[LicenceModel] | str
    anti_patterns: list[AntiPatternModel]
    complexity: float
    energy_consumption_kwh: float
    carbon_emission_gco2e: float
    quality_gate: QualityGateModel
    certificate: CertificateModel | None = None


# Model used to create the audit of a project
class AuditCreateModel(BaseModel):
    """
    Model used to create the audit of a project.

    Attributes
    ----------
    project : ProjectCompletedModel
        Project to audit, with its code and dependency files.
    qualitygate_type : {'eco', 'security', 'global'}
        Type of quality gate to apply.
    hmac_signature : str
        HMAC signature of the request, encoded in Base64.
    """

    project: ProjectCompletedModel
    qualitygate_type: Literal["eco", "security", "global"]
    hmac_signature: str
