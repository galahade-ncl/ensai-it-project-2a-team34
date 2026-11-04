from datetime import datetime

from pydantic import BaseModel

from schema.certificate_model import CertificateModel
from schema.qualitygate_model import QualityGateModel
from schema.sbom_model import SbomModel


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
    vulnerabilities: list
    licenses: list
    anti_patterns: list
    complexity: float
    energy_consumption_kwh: float
    carbon_emission_gco2e: float
    sbom: SbomModel
    quality_gate: QualityGateModel
    certificate: CertificateModel


# Model used to create the audit of a project
class AuditCreateModel(BaseModel):
    id_project: int
    qualitygate_type: str
    hmac_signature: str
