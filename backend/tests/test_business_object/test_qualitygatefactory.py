import pytest

from business_object.qualitygate.ecoqualitygate import EcoQualityGate
from business_object.qualitygate.globalqualitygate import GlobalQualityGate
from business_object.qualitygate.qualitygatefactory import QualityGateFactory
from business_object.qualitygate.securityqualitygate import SecurityQualityGate


@pytest.mark.parametrize(
    "kind, cls",
    [("eco", EcoQualityGate), ("SECURITY", SecurityQualityGate), ("global", GlobalQualityGate)],
)
def test_returns_right_class(kind, cls):
    gate = QualityGateFactory.get_qualitygate(kind, 5, 0, 1, 0.001, "Unevaluated")
    assert isinstance(gate, cls)


def test_unknown_type_raises():
    with pytest.raises(ValueError):
        QualityGateFactory.get_qualitygate("MIGUEL", 5, 0, 1, 0.001, "Unevaluated")


# (max_vulnerabilities, max_critical_vulnerabilities, max_carbon_emission,
#  max_energy_consumption, status)
THRESHOLDS = [
    (10, 5, 50, 200, "Passed"),
    (10, 5, 5000, 1000000, "Failed"),
    (60, 20, 0, 0, "Unevaluated"),
    (0, 0, 0, 0, "Unevaluated"),
    (2, 0, 2, 30, "Passed"),
    (8, 1, 2, 0.111, "Failed"),
]


@pytest.mark.parametrize("max_vuln, max_crit, max_carbon, max_energy, status", THRESHOLDS)
def test_get_qualitygate_eco(max_vuln, max_crit, max_carbon, max_energy, status):
    """Successfully create an EcoQualityGate"""

    # GIVEN
    qualitygate_type = "eco"

    # WHEN
    qualitygate = QualityGateFactory.get_qualitygate(
        qualitygate_type, max_vuln, max_crit, max_carbon, max_energy, status
    )

    # THEN
    assert isinstance(qualitygate, EcoQualityGate)
    assert qualitygate.get_type() == "eco"
    assert qualitygate.max_carbon_emission == max_carbon
    assert qualitygate.max_energy_consumption == max_energy
    assert qualitygate.status == status


@pytest.mark.parametrize("max_vuln, max_crit, max_carbon, max_energy, status", THRESHOLDS)
def test_get_qualitygate_security(max_vuln, max_crit, max_carbon, max_energy, status):
    """Successfully create a SecurityQualityGate"""

    # GIVEN
    qualitygate_type = "security"

    # WHEN
    qualitygate = QualityGateFactory.get_qualitygate(
        qualitygate_type, max_vuln, max_crit, max_carbon, max_energy, status
    )

    # THEN
    assert isinstance(qualitygate, SecurityQualityGate)
    assert qualitygate.get_type() == "security"
    assert qualitygate.max_vulnerabilities == max_vuln
    assert qualitygate.max_critical_vulnerabilities == max_crit
    assert qualitygate.status == status


@pytest.mark.parametrize("max_vuln, max_crit, max_carbon, max_energy, status", THRESHOLDS)
def test_get_qualitygate_global(max_vuln, max_crit, max_carbon, max_energy, status):
    """Successfully create a GlobalQualityGate"""

    # GIVEN
    qualitygate_type = "global"

    # WHEN
    qualitygate = QualityGateFactory.get_qualitygate(
        qualitygate_type, max_vuln, max_crit, max_carbon, max_energy, status
    )

    # THEN
    assert isinstance(qualitygate, GlobalQualityGate)
    assert qualitygate.get_type() == "global"
    assert qualitygate.max_vulnerabilities == max_vuln
    assert qualitygate.max_critical_vulnerabilities == max_crit
    assert qualitygate.max_carbon_emission == max_carbon
    assert qualitygate.max_energy_consumption == max_energy
    assert qualitygate.status == status


@pytest.mark.parametrize(
    "qualitygate_type, expected_class",
    [
        ("eco", EcoQualityGate),
        ("ECO", EcoQualityGate),
        ("Security", SecurityQualityGate),
        ("GLOBAL", GlobalQualityGate),
    ],
)
def test_get_qualitygate_is_case_insensitive(qualitygate_type, expected_class):
    """The type of the QualityGate is not case-sensitive"""

    # WHEN
    qualitygate = QualityGateFactory.get_qualitygate(
        qualitygate_type, 5, 0, 1, 0.001, "Unevaluated"
    )

    # THEN
    assert isinstance(qualitygate, expected_class)


@pytest.mark.parametrize("qualitygate_type", ["test_de_faux_qualitygate_type", "", "ecoo"])
def test_get_qualitygate_false_type(qualitygate_type):
    """The type_qualitygate is not valid"""

    # WHEN / THEN
    with pytest.raises(ValueError, match="not supported"):
        QualityGateFactory.get_qualitygate(qualitygate_type, 5, 0, 1, 0.001, "Unevaluated")
