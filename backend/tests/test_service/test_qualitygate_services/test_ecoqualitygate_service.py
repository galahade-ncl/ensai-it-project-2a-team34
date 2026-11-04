from unittest.mock import MagicMock

from src.business_object.qualitygate.ecoqualitygate import EcoQualityGate
from src.service.qualitygate_services.ecoqualitygate_service import EcoQualityGateService

qualitygatelist = [
    EcoQualityGate(
        max_carbon_emission=50,
        max_energy_consumption=200,
        status="Passed",
    ),
    EcoQualityGate(max_carbon_emission=5000, max_energy_consumption=1000000, status="Failed"),
    EcoQualityGate(max_carbon_emission=1000000, max_energy_consumption=2, status="Passed"),
    EcoQualityGate(
        max_carbon_emission=0,
        max_energy_consumption=0,
        status="Unevaluated",
    ),
    EcoQualityGate(max_carbon_emission=2, max_energy_consumption=30, status="Passed"),
    EcoQualityGate(max_carbon_emission=2, max_energy_consumption=1000000, status="Unevaluated"),
]


def test_create_successful():
    """Successfully create a EcoQualityGate object"""

    for i in range(6):
        # GIVEN
        qualitygate_expected = qualitygatelist[i]
        EcoQualityGate.create = MagicMock(return_value=qualitygate_expected)

        # WHEN
        response_qualitygate = EcoQualityGateService().create(
            qualitygate_expected.max_carbon_emission,
            qualitygate_expected.max_energy_consumption,
            qualitygate_expected.status,
        )

        # THEN
        assert response_qualitygate.get_type() == "eco"
        assert response_qualitygate.max_carbon_emission == qualitygate_expected.max_carbon_emission
        assert (
            response_qualitygate.max_energy_consumption
            == qualitygate_expected.max_energy_consumption
        )
        assert response_qualitygate.status == qualitygate_expected.status
