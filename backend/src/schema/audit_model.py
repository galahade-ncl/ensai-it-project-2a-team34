from datetime import datetime

from pydantic import BaseModel

from schema.antipattern_model import AntiPatternModel
from schema.certificate_model import CertificateModel
from schema.licence_model import LicenceModel
from schema.project_model import ProjectCompletedModel
from schema.qualitygate_model import QualityGateModel
from schema.sbom_model import SbomModel
from schema.vulnerability_model import VulnerabilityModel


# When the user wants information on a past audit
class AuditReadModel(BaseModel):
    id_audit: int
    id_project: int
    date: datetime
    complexity: float
    energy_consumption_kwh: float
    carbon_emission_gco2e: float
    quality_gate: QualityGateModel


# When user runs an audit on a project
class AuditResponseModel(BaseModel):
    id_audit: int
    id_project: int
    date: datetime
    vulnerabilities: list[VulnerabilityModel]
    licenses: list[LicenceModel] | str
    anti_patterns: list[AntiPatternModel]
    complexity: float
    energy_consumption_kwh: float
    carbon_emission_gco2e: float
    sbom: SbomModel
    quality_gate: QualityGateModel
    certificate: CertificateModel | None = None


# Model used to create the audit of a project
class AuditCreateModel(BaseModel):
    project: ProjectCompletedModel
    qualitygate_type: str
    hmac_signature: str
