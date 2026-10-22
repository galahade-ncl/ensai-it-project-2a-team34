from datetime import datetime

from pydantic import BaseModel

from business_object.certificate import Certificate
from business_object.qualitygate import QualityGate


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
    #sbom: SBOM
    quality_gate: QualityGate
    certificate: Certificate


class AuditCreateModel(BaseModel):
    id_project: int
    date: datetime
