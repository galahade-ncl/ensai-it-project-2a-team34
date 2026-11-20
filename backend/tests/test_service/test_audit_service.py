import datetime
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from business_object.audit import Audit
from business_object.project import Project
from dao.audit_dao import AuditDao
from service.audit_service import AuditService
from service.eco_service import EcoService
from service.qualitygate_service import QualityGateService
from service.sbom_service import SBOMService
from service.security_service import SecurityService


def _audit():
    return Audit(
        id_project=10,
        date=datetime.datetime(2025, 1, 15),
        vulnerabilities=[],
        licenses=[],
        anti_patterns=[],
        complexity=4.2,
        energy_consumption_kwh=0.35,
        carbon_emission_gco2e=12.5,
        sbom=MagicMock(),
        quality_gate=MagicMock(),
        certificate=None,
    )


def test_create_successful():
    date = datetime.datetime(2025, 1, 15)
    vulnerabilities, licenses, anti_patterns = [], [], []
    sbom, quality_gate, certificate = MagicMock(), MagicMock(), MagicMock()

    with patch.object(AuditDao, "create", return_value=True) as dao_create:
        audit = AuditService().create(
            10,
            date,
            vulnerabilities,
            licenses,
            anti_patterns,
            4.2,
            0.35,
            12.5,
            sbom,
            quality_gate,
            certificate,
        )

    assert audit is not None
    assert audit.id_project == 10
    assert audit.date == date
    assert audit.complexity == 4.2
    assert audit.energy_consumption_kwh == 0.35
    assert audit.carbon_emission_gco2e == 12.5
    dao_create.assert_called_once()


def test_create_failed():
    with patch.object(AuditDao, "create", return_value=False) as dao_create:
        audit = AuditService().create(
            10,
            datetime.datetime(2025, 1, 15),
            [],
            [],
            [],
            4.2,
            0.35,
            12.5,
            MagicMock(),
            MagicMock(),
            None,
        )

    assert audit is None
    dao_create.assert_called_once()


def test_find_by_id_successful():
    expected = _audit()
    with patch.object(AuditDao, "find_by_id", return_value=expected) as dao_find:
        result = AuditService().find_by_id(1)

    assert result == expected
    dao_find.assert_called_once_with(1)


def test_find_by_id_failed():
    with patch.object(AuditDao, "find_by_id", return_value=None) as dao_find:
        result = AuditService().find_by_id(555)

    assert result is None
    dao_find.assert_called_once_with(555)


def test_list_all_audit_successful():
    expected = [_audit(), _audit()]
    with patch.object(AuditDao, "find_all", return_value=expected) as dao_find:
        result = AuditService().list_all_audit(10)

    assert result == expected
    assert len(result) == 2
    dao_find.assert_called_once_with(10)


def test_list_all_audit_empty():
    with patch.object(AuditDao, "find_all", return_value=[]) as dao_find:
        result = AuditService().list_all_audit(10)

    assert result == []
    dao_find.assert_called_once_with(10)


def _project():
    project = Project(
        id_project=1,
        name_project="project_numero_1",
        secretHMACkey=bytes.fromhex(
            "7f2cd2cada12a1c7f6550f4b9aa3873776d6b0228b2d9c1596dcdf8eda301930"
        ),
    )
    project.dependencyfile = MagicMock()
    project.codefile = MagicMock()
    return project


def test_run_audit_successful():
    project = _project()
    vulnerabilities = [MagicMock(), MagicMock()]
    licenses = [MagicMock()]
    anti_patterns = [MagicMock(), MagicMock()]
    sbom = MagicMock()
    quality_gate = MagicMock()
    analysis = SimpleNamespace(
        antipatterns=anti_patterns,
        complexity=4.2,
        energy_kwh=0.35,
        carbon_gco2e=12.5,
    )

    with (
        patch.object(SecurityService, "find_vulnerabilities", return_value=vulnerabilities) as find_vuln,
        patch.object(SecurityService, "find_licences", return_value=licenses) as find_licenses,
        patch.object(EcoService, "analyze", return_value=analysis) as analyze,
        patch.object(SBOMService, "generate", return_value=sbom) as generate_sbom,
        patch.object(QualityGateService, "create", return_value=quality_gate) as create_gate,
        patch.object(QualityGateService, "evaluate") as evaluate_gate,
        patch.object(AuditDao, "create", return_value=True) as dao_create,
        patch.object(AuditDao, "update", return_value=True) as dao_update,
    ):
        audit = AuditService().run_audit(project, "global")

    assert audit is not None
    assert audit.id_project == project.id_project
    assert audit.vulnerabilities == vulnerabilities
    assert audit.licenses == licenses
    assert audit.anti_patterns == anti_patterns
    assert audit.energy_consumption_kwh == 0.35
    assert audit.carbon_emission_gco2e == 12.5
    assert audit.sbom == sbom
    assert audit.quality_gate == quality_gate

    find_vuln.assert_called_once_with(project.dependencyfile)
    find_licenses.assert_called_once_with(project.dependencyfile)
    analyze.assert_called_once_with(project.codefile)
    generate_sbom.assert_called_once_with(project, vulnerabilities)
    create_gate.assert_called_once_with(
        "global",
        max_vulnerabilities=5,
        max_critical_vulnerabilities=0,
        max_carbon_emission=1,
        max_energy_consumption=0.001,
        status="Unevaluated",
    )
    evaluate_gate.assert_called_once_with(quality_gate, audit)
    dao_create.assert_called_once()
    dao_update.assert_called_once()


def test_run_audit_dao_create_fails():
    project = _project()
    analysis = SimpleNamespace(
        antipatterns=[],
        complexity=1.0,
        energy_kwh=0.1,
        carbon_gco2e=5.0,
    )

    with (
        patch.object(SecurityService, "find_vulnerabilities", return_value=[]),
        patch.object(SecurityService, "find_licences", return_value=[]),
        patch.object(EcoService, "analyze", return_value=analysis),
        patch.object(SBOMService, "generate", return_value=MagicMock()),
        patch.object(QualityGateService, "create", return_value=MagicMock()),
        patch.object(QualityGateService, "evaluate"),
        patch.object(AuditDao, "create", return_value=False) as dao_create,
    ):
        audit = AuditService().run_audit(project, "global")

    assert audit is None
    dao_create.assert_called_once()
