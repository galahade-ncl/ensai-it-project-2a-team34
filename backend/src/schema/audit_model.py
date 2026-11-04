from datetime import datetime

from pydantic import BaseModel

from schema.certificate_model import CertificateModel
from schema.qualitygate_model import QualityGateModel


class AuditResponseModel(BaseModel):
    id_audit: int
    id_project: int
    date: datetime


class AuditReadModel(BaseModel):
    id_audit: int
    id_project: int
    date: datetime
    vulnerabilities: list
    licenses: list
    anti_patterns: list
    complexity: float
    energy_consumption_kwh: float
    carbon_emission_gco2e: float
    # sbom: SBOM
    quality_gate: QualityGateModel
    certificate: CertificateModel


# Model used to create the audit of a project
class AuditCreateModel(BaseModel):
    id_project: int
    quality_gate_type: str
    hmac_signature: str
