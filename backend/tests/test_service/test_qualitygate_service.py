from datetime import datetime
from unittest.mock import MagicMock

from src.business_object.audit import Audit
from src.business_object.qualitygate.ecoqualitygate import EcoQualityGate
from src.business_object.qualitygate.globalqualitygate import GlobalQualityGate
from src.business_object.qualitygate.qualitygate import QualityGate
from src.business_object.qualitygate.securityqualitygate import SecurityQualityGate
from src.business_object.vulnerability.critical_vulnerability import CriticalVulnerability
from src.business_object.vulnerability.high_vulnerability import HighVulnerability
from src.business_object.vulnerability.low_vulnerability import LowVulnerability
from src.business_object.vulnerability.medium_vulnerability import MediumVulnerability
from src.service.qualitygate_service import QualityGateService

qualitygatelist = [
    GlobalQualityGate(
        max_vulnerabilities=10,
        max_critical_vulnerabilities=5,
        max_carbon_emission=50,
        max_energy_consumption=200,
        status="Passed",
    ),
    EcoQualityGate(max_carbon_emission=5000, max_energy_consumption=1000000, status="Failed"),
    SecurityQualityGate(max_vulnerabilities=60, max_critical_vulnerabilities=20, status="Passed"),
    GlobalQualityGate(
        max_vulnerabilities=0,
        max_critical_vulnerabilities=0,
        max_carbon_emission=0,
        max_energy_consumption=0,
        status="Failed",
    ),
    EcoQualityGate(max_carbon_emission=2, max_energy_consumption=30, status="Passed"),
    SecurityQualityGate(max_vulnerabilities=8, max_critical_vulnerabilities=1, status="Failed"),
]

audit = Audit(
    id_audit=1,
    id_project=42,
    date=datetime(2026, 10, 9, 14, 35, 27),
    vulnerabilities=[
        HighVulnerability(
            id_vulnerability=1,
            osv_id="GHSA-jfh8-c2jp-5v3q",
            cve_id="CVE-2021-44228",
            package="log4j-core",
            version_package="2.14.1",
        ),
        LowVulnerability(
            id_vulnerability=2,
            osv_id="GHSA-74fj-2j2h-c42q",
            cve_id="CVE-2023-32681",
            package="requests",
            version_package="2.30.0",
        ),
        CriticalVulnerability(
            id_vulnerability=3,
            osv_id="GHSA-3ppc-4f35-3m26",
            cve_id="CVE-2022-40897",
            package="setuptools",
            version_package="65.5.0",
        ),
        CriticalVulnerability(
            id_vulnerability=4,
            osv_id="GHSA-59g5-xgcq-4qw3",
            cve_id="CVE-2023-45803",
            package="urllib3",
            version_package="1.26.17",
        ),
        MediumVulnerability(
            id_vulnerability=5,
            osv_id="GHSA-9wx4-h78v-vm56",
            cve_id="CVE-2024-35195",
            package="requests",
            version_package="2.31.0",
        ),
        MediumVulnerability(
            id_vulnerability=6,
            osv_id="GHSA-4xh5-x5gv-qwph",
            cve_id="CVE-2024-3651",
            package="idna",
            version_package="3.6",
        ),
    ],
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
    GlobalQualityGate.evaluate = MagicMock(return_value=True)
    EcoQualityGate.evaluate = MagicMock(return_value=True)
    SecurityQualityGate.evaluate = MagicMock(return_value=True)

    for i in range(3):
        # WHEN
        QualityGateService().evaluate(qualitygate=qualitygatelist[i], audit=audit)

        # THEN
        assert audit.quality_gate.status == "Passed"


def test_evaluate_failed():
    """Fail to evaluate a Project during an Audit with the QualityGate chosen because QualityGate().evaluate returns False"""

    # GIVEN
    GlobalQualityGate.evaluate = MagicMock(return_value=False)
    EcoQualityGate.evaluate = MagicMock(return_value=False)
    SecurityQualityGate.evaluate = MagicMock(return_value=False)

    for i in range(3, 6):
        # WHEN
        QualityGateService().evaluate(qualitygate=qualitygatelist[i], audit=audit)

        # THEN
        assert audit.quality_gate.status == "Failed"
