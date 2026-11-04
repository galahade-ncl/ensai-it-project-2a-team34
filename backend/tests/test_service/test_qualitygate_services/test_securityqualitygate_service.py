from unittest.mock import MagicMock

from src.business_object.qualitygate.securityqualitygate import SecurityQualityGate
from src.service.qualitygate_services.securityqualitygate_service import SecurityQualityGateService

qualitygatelist_service = [
    SecurityQualityGate(
        max_vulnerabilities=10,
        max_critical_vulnerabilities=1,
        status="Passed",
    ),
    SecurityQualityGate(
        max_vulnerabilities=10,
        max_critical_vulnerabilities=9,
        status="Failed"),
    SecurityQualityGate(
        max_vulnerabilities=60,
        max_critical_vulnerabilities=20,
        status="Unevaluated"),
    SecurityQualityGate(
        max_vulnerabilities=0,
        max_critical_vulnerabilities=0,
        status="Unevaluated",
    ),
    SecurityQualityGate(
        max_vulnerabilities=2,
        max_critical_vulnerabilities=0,
        status="Passed"),
    SecurityQualityGate(
        max_vulnerabilities=150,
        max_critical_vulnerabilities=1,
        status="Failed"),
]


def test_create_successful(monkeypatch):
    """Successfully create a SecurityQualityGate object"""

    for i in range(6):
        # GIVEN
        qualitygate_expected = qualitygatelist_service[i]
        monkeypatch.setattr(SecurityQualityGate, "evaluate", MagicMock(return_value=True))

        # WHEN
        response_qualitygate = SecurityQualityGateService().create(
            max_vulnerabilities=qualitygate_expected.max_vulnerabilities,
            max_critical_vulnerabilities=qualitygate_expected.max_critical_vulnerabilities,
            status=qualitygate_expected.status,
        )

        # THEN
        assert response_qualitygate.max_vulnerabilities == qualitygate_expected.max_vulnerabilities, (
    f"i={i}, got={response_qualitygate.max_vulnerabilities}, "
    f"expected={qualitygate_expected.max_vulnerabilities}")
        assert response_qualitygate.get_type() == "security"
        assert response_qualitygate.max_vulnerabilities == qualitygate_expected.max_vulnerabilities
        assert response_qualitygate.max_critical_vulnerabilities == qualitygate_expected.max_critical_vulnerabilities
        assert response_qualitygate.status == qualitygate_expected.status
