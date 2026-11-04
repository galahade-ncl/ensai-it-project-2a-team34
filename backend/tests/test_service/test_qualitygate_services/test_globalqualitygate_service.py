from unittest.mock import MagicMock

from src.business_object.qualitygate.globalqualitygate import GlobalQualityGate
from src.service.qualitygate_services.globalqualitygate_service import GlobalQualityGateService

qualitygatelist = [
    GlobalQualityGate(
        max_vulnerabilities=10,
        max_critical_vulnerabilities=5,
        max_carbon_emission=50,
        max_energy_consumption=200,
        status="Passed",
    ),
    GlobalQualityGate(
        max_vulnerabilities=10,
        max_critical_vulnerabilities=5,
        max_carbon_emission=5000,
        max_energy_consumption=1000000,
        status="Failed"),
    GlobalQualityGate(
        max_vulnerabilities=60,
        max_critical_vulnerabilities=20,
        max_carbon_emission=0,
        max_energy_consumption=0,
        status="Unevaluated"),
    GlobalQualityGate(
        max_vulnerabilities=0,
        max_critical_vulnerabilities=0,
        max_carbon_emission=0,
        max_energy_consumption=0,
        status="Unevaluated",
    ),
    GlobalQualityGate(
        max_vulnerabilities=2,
        max_critical_vulnerabilities=0,
        max_carbon_emission=2,
        max_energy_consumption=30,
        status="Passed"),
    GlobalQualityGate(
        max_vulnerabilities=8,
        max_critical_vulnerabilities=1,
        max_carbon_emission=2,
        max_energy_consumption=0.111,
        status="Failed"),
]


def test_create_successful(monkeypatch):
    """Successfully create a GlobalQualityGate object"""

    for i in range(6):
        # GIVEN
        qualitygate_expected = qualitygatelist[i]
        monkeypatch.setattr(GlobalQualityGate, "evaluate", MagicMock(return_value=True))
        # WHEN
        response_qualitygate = GlobalQualityGateService().create(
            qualitygate_expected.max_vulnerabilities,
            qualitygate_expected.max_critical_vulnerabilities,
            qualitygate_expected.max_carbon_emission,
            qualitygate_expected.max_energy_consumption,
            qualitygate_expected.status,
        )

        # THEN
        assert response_qualitygate.get_type() == "global"
        assert response_qualitygate.max_vulnerabilities == qualitygate_expected.max_vulnerabilities
        assert response_qualitygate.max_critical_vulnerabilities == qualitygate_expected.max_critical_vulnerabilities
        assert response_qualitygate.max_carbon_emission == qualitygate_expected.max_carbon_emission
        assert response_qualitygate.max_energy_consumption == qualitygate_expected.max_energy_consumption
        assert response_qualitygate.status == qualitygate_expected.status
