from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from business_object.audit import Audit
from business_object.qualitygate.ecoqualitygate import EcoQualityGate
from business_object.qualitygate.globalqualitygate import GlobalQualityGate
from business_object.qualitygate.qualitygatefactory import QualityGateFactory
from business_object.qualitygate.securityqualitygate import SecurityQualityGate
from service.qualitygate_service import QualityGateService

MODULE = "service.qualitygate_service"


def make_audit() -> Audit:
    """Minimal audit: its content is irrelevant because evaluate() is mocked."""
    return Audit(
        id_project=1,
        date=datetime(2026, 10, 9, 14, 35, 27),
        vulnerabilities=[],
        licenses=[],
        anti_patterns=[],
        complexity=1,
        energy_consumption_kwh=0.0,
        carbon_emission_gco2e=0.0,
        sbom=None,
        quality_gate=None,
        certificate=None,
    )


@pytest.mark.parametrize(
    "qualitygate_type, expected_class",
    [
        ("eco", EcoQualityGate),
        ("security", SecurityQualityGate),
        ("global", GlobalQualityGate),
    ],
)
def test_create_successful(qualitygate_type, expected_class):
    """Successfully create a QualityGate object"""

    # WHEN
    qualitygate = QualityGateService().create(qualitygate_type, 5, 0, 1, 0.001, "Unevaluated")

    # THEN
    assert isinstance(qualitygate, expected_class)
    assert qualitygate.get_type() == qualitygate_type
    assert qualitygate.status == "Unevaluated"


def test_create_delegates_to_factory():
    """The creation of the QualityGate is delegated to the factory"""

    # GIVEN
    with patch(f"{MODULE}.QualityGateFactory") as factory:
        # WHEN
        response = QualityGateService().create("eco", 5, 0, 1, 0.001, "Unevaluated")

        # THEN
        factory.get_qualitygate.assert_called_once_with("eco", 5, 0, 1, 0.001, "Unevaluated")
        assert response is factory.get_qualitygate.return_value


def test_create_false_type_qualitygate():
    """The type_qualitygate is not valid"""

    # GIVEN
    qualitygate_type = "test_de_faux_qualitygate_type"

    # WHEN / THEN
    with pytest.raises(ValueError):
        QualityGateService().create(
            type_qualitygate=qualitygate_type,
            max_vulnerabilities=0,
            max_critical_vulnerabilities=0,
            max_carbon_emission=0,
            max_energy_consumption=0,
            status="Unevaluated",
        )


@pytest.mark.parametrize("qualitygate_type", ["eco", "security", "global"])
def test_evaluate_successful(monkeypatch, qualitygate_type):
    """The Project passed the QualityGate successfully"""

    # GIVEN
    qualitygate = QualityGateFactory.get_qualitygate(
        qualitygate_type, 5, 0, 1, 0.001, "Unevaluated"
    )
    fake_evaluate = MagicMock(return_value=True)
    monkeypatch.setattr(qualitygate, "evaluate", fake_evaluate)  # restored after the test
    audit = make_audit()

    # WHEN
    QualityGateService().evaluate(qualitygate, audit)

    # THEN
    assert audit.quality_gate is qualitygate
    assert audit.quality_gate.status == "Passed"
    fake_evaluate.assert_called_once_with(audit)


@pytest.mark.parametrize("qualitygate_type", ["eco", "security", "global"])
def test_evaluate_failed(monkeypatch, qualitygate_type):
    """The Project failed to pass the QualityGate"""

    # GIVEN
    qualitygate = QualityGateFactory.get_qualitygate(
        qualitygate_type, 5, 0, 1, 0.001, "Unevaluated"
    )
    fake_evaluate = MagicMock(return_value=False)
    monkeypatch.setattr(qualitygate, "evaluate", fake_evaluate)  # restored after the test
    audit = make_audit()

    # WHEN
    QualityGateService().evaluate(qualitygate, audit)

    # THEN
    assert audit.quality_gate is qualitygate
    assert audit.quality_gate.status == "Failed"
    fake_evaluate.assert_called_once_with(audit)
