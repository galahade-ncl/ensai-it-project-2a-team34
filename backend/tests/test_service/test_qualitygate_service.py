from datetime import datetime
from unittest.mock import MagicMock

from src.business_object.audit import Audit
from src.business_object.qualitygate.ecoqualitygate import EcoQualityGate
from src.business_object.qualitygate.globalqualitygate import GlobalQualityGate
from src.business_object.qualitygate.qualitygate import QualityGate
from src.business_object.qualitygate.securityqualitygate import SecurityQualityGate
from src.service.qualitygate_service import QualityGateService

qualitygatelist = [
    GlobalQualityGate(
        max_vulnerabilities=2,
        max_critical_vulnerabilities=0,
        max_carbon_emission=50,
        max_energy_consumption=200,
        status="Passed",
    ),
    GlobalQualityGate(
        max_vulnerabilities=0,
        max_critical_vulnerabilities=0,
        max_carbon_emission=0,
        max_energy_consumption=0,
        status="Failed",
    ),
    EcoQualityGate(max_carbon_emission=5000, max_energy_consumption=1000000, status="Passed"),
    EcoQualityGate(max_carbon_emission=20, max_energy_consumption=30, status="Failed"),
    SecurityQualityGate(max_vulnerabilities=60, max_critical_vulnerabilities=20, status="Passed"),
    SecurityQualityGate(max_vulnerabilities=1, max_critical_vulnerabilities=0, status="Failed"),
]

audit = Audit(
    id_audit=1,
    id_project=42,
    date=datetime(2026, 10, 9, 14, 35, 27),
    vulnerabilities=[],
    licenses=["MIT", "Apache-2.0"],
    anti_patterns=[],
    complexity=10,
    energy_consumption_kwh=0.15,
    carbon_emission_gco2e=12.5,
    sbom={"components": []},
    quality_gate=None,
    certificate=None,
)


def test_evaluate_successful():
    """Successfully evaluate a Project during an Audit with the QualityGate chosen"""

    # GIVEN
    QualityGate.evaluate = MagicMock(return_value=True)

    # WHEN
    QualityGateService().evaluate(qualitygate=qualitygatelist[1], audit=audit)

    # THEN
    assert audit.quality_gate.status == "Passed"


def test_evaluate_failed():
    """Fail to evaluate a Project during an Audit with the QualityGate chosen because QualityGate().evaluate returns False"""

    # GIVEN
    QualityGate.evaluate = MagicMock(return_value=False)

    # WHEN
    QualityGateService().evaluate(qualitygate=qualitygatelist[4], audit=audit)

    # THEN
    assert audit.quality_gate.status == "Failed"
