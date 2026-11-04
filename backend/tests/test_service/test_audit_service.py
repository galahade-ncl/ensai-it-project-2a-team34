import datetime
from unittest.mock import MagicMock, patch

from business_object.audit import Audit
from business_object.file.sbomfile import SBOMFile
from business_object.project import Project
from business_object.qualitygate.qualitygate import QualityGate
from business_object.user import User
from dao.audit_dao import AuditDao
from service.audit_service import AuditService
from service.eco_service import EcoService
from service.qualitygate_services.qualitygate_service import QualityGateService
from service.sbom_service import SBOMService
from service.security_service import SecurityService

# from business_object.file.certificatefile import CertificateFile


def test_create_successful():
    """Successfully create an Audit"""

    # GIVEN
    id_audit, id_project = 1, 10
    date = datetime.datetime(2025, 1, 15)
    vulnerabilities, licenses, anti_patterns = [], [], []
    certificate = MagicMock()
    complexity, energy_consumption_kwh, carbon_emission_gco2e = 4.2, 0.35, 12.5
    sbom = MagicMock()
    quality_gate = MagicMock()
    AuditDao.create = MagicMock(return_value=True)

    # WHEN
    audit = AuditService().create(
        id_audit,
        id_project,
        date,
        vulnerabilities,
        licenses,
        anti_patterns,
        complexity,
        energy_consumption_kwh,
        carbon_emission_gco2e,
        sbom,
        quality_gate,
        certificate,
    )

    # THEN
    assert audit is not None
    assert audit.id_project == id_project
    assert audit.date == date
    assert audit.complexity == complexity
    assert audit.energy_consumption_kwh == energy_consumption_kwh
    assert audit.carbon_emission_gco2e == carbon_emission_gco2e
    AuditDao.create.assert_called_once()


def test_create_failed():
    """Failed to create an Audit because AuditDao().create returns False"""

    # GIVEN
    id_audit, id_project = 1, 10
    date = datetime.datetime(2025, 1, 15)
    vulnerabilities, licenses, anti_patterns = [], [], []
    certificate = MagicMock()
    complexity, energy_consumption_kwh, carbon_emission_gco2e = 4.2, 0.35, 12.5
    sbom = MagicMock()
    quality_gate = MagicMock()
    AuditDao.create = MagicMock(return_value=False)

    # WHEN
    audit = AuditService().create(
        id_audit,
        id_project,
        date,
        vulnerabilities,
        licenses,
        anti_patterns,
        complexity,
        energy_consumption_kwh,
        carbon_emission_gco2e,
        sbom,
        quality_gate,
        certificate,
    )

    # THEN
    assert audit is None
    AuditDao.create.assert_called_once()


def test_find_by_id_successful():
    """Successfully find the audit"""

    # GIVEN
    audit = Audit(
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
        certificate=[],
    )
    AuditDao.find_by_id = MagicMock(return_value=audit)

    # WHEN
    res = AuditService().find_by_id(1)

    # THEN
    assert res == audit
    AuditDao.find_by_id.assert_called_once_with(1)


def test_find_by_id_failed():
    """Fail to find the audit"""

    # GIVEN
    AuditDao.find_by_id = MagicMock(return_value=None)

    # WHEN
    res = AuditService().find_by_id(555)

    # THEN
    assert res is None
    AuditDao.find_by_id.assert_called_once_with(555)


def test_list_all_audit_successful():
    """Successfully list all the audits of a project"""

    # GIVEN
    audit1 = Audit(
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
        certificate=[],
    )
    audit2 = Audit(
        id_project=10,
        date=datetime.datetime(2025, 2, 20),
        vulnerabilities=[],
        licenses=[],
        anti_patterns=[],
        complexity=3.8,
        energy_consumption_kwh=0.30,
        carbon_emission_gco2e=10.0,
        sbom=MagicMock(),
        quality_gate=MagicMock(),
        certificate=[],
    )
    AuditDao.find_all = MagicMock(return_value=[audit1, audit2])

    # WHEN
    res = AuditService().list_all_audit(10)

    # THEN
    assert res == [audit1, audit2]
    assert len(res) == 2
    AuditDao.find_all.assert_called_once_with(10)


def test_list_all_audit_empty():
    """Return an empty list when the project has no audit"""

    # GIVEN
    AuditDao.find_all = MagicMock(return_value=[])

    # WHEN
    res = AuditService().list_all_audit(10)

    # THEN
    assert res == []
    AuditDao.find_all.assert_called_once_with(10)


def test_run_audit_successful():
    """Successfully runs an audit on a project"""

    # GIVEN
    project = Project(
        id_project=1,
        name_project="project_numero_1",
        user=User(id_user=1, username="Jean-michel", email="jean-michel@mail.fr", password="0000"),
        secretHMACkey=bytes.fromhex(
            "7f2cd2cada12a1c7f6550f4b9aa3873776d6b0228b2d9c1596dcdf8eda301930"
        ),
    )
    project.dependencyfile = MagicMock()
    project.codefile = MagicMock()

    mock_vulnerabilities = [MagicMock(), MagicMock()]
    mock_licenses = [MagicMock()]
    mock_antipatterns = [MagicMock(), MagicMock(), MagicMock()]
    mock_energy = 0.35
    mock_carbon = 12.5
    mock_sbom = MagicMock(spec=SBOMFile)
    mock_quality_gate = MagicMock(spec=QualityGate)

    with (
        patch.object(
            SecurityService, "find_vulnerabilities", return_value=mock_vulnerabilities
        ) as mock_find_vuln,
        patch.object(SecurityService, "find_licences", return_value=mock_licenses) as mock_find_lic,
        patch.object(
            EcoService, "detect_antipatterns", return_value=mock_antipatterns
        ) as mock_detect_ap,
        patch.object(EcoService, "calculate_energy", return_value=mock_energy) as mock_calc_energy,
        patch.object(EcoService, "calculate_carbon", return_value=mock_carbon) as mock_calc_carbon,
        patch.object(SBOMService, "generate", return_value=mock_sbom) as mock_generate_sbom,
        patch.object(
            QualityGateService, "create", return_value=mock_quality_gate
        ) as mock_create_qg,
        patch.object(QualityGateService, "evaluate") as mock_evaluate_qg,
        patch.object(AuditDao, "create", return_value=True) as mock_dao_create,
    ):
        # WHEN
        audit = AuditService().run_audit(project, "global")

        # THEN
        assert audit is not None
        assert audit.id_project == project.id_project
        assert audit.vulnerabilities == mock_vulnerabilities
        assert audit.licenses == mock_licenses
        assert audit.anti_patterns == mock_antipatterns
        assert audit.energy_consumption_kwh == mock_energy
        assert audit.carbon_emission_gco2e == mock_carbon
        assert audit.sbom == mock_sbom
        assert audit.quality_gate == mock_quality_gate

        mock_find_vuln.assert_called_once_with(project.dependencyfile)
        mock_find_lic.assert_called_once_with(project.dependencyfile)
        mock_detect_ap.assert_called_once_with(project.codefile)
        mock_calc_energy.assert_called_once_with(project.codefile)
        mock_calc_carbon.assert_called_once_with(mock_energy)
        mock_generate_sbom.assert_called_once_with(project)
        mock_create_qg.assert_called_once_with(
            "global",
            max_vulnerabilities=5,
            max_critical_vulnerabilities=0,
            max_carbon_emission=1,
            max_energy_consumption=0.001,
        )
        mock_evaluate_qg.assert_called_once_with(mock_quality_gate, audit)
        mock_dao_create.assert_called_once()


def test_run_audit_dao_create_fails():
    """run_audit returns None when AuditDao.create fails"""

    # GIVEN
    project = Project(
        id_project=1,
        name_project="project_numero_1",
        user=User(id_user=1, username="Jean-michel", email="jean-michel@mail.fr", password="0000"),
        secretHMACkey=bytes.fromhex(
            "7f2cd2cada12a1c7f6550f4b9aa3873776d6b0228b2d9c1596dcdf8eda301930"
        ),
    )
    project.dependencyfile = MagicMock()
    project.codefile = MagicMock()

    with (
        patch.object(SecurityService, "find_vulnerabilities", return_value=[]),
        patch.object(SecurityService, "find_licences", return_value=[]),
        patch.object(EcoService, "detect_antipatterns", return_value=[]),
        patch.object(EcoService, "calculate_energy", return_value=0.1),
        patch.object(EcoService, "calculate_carbon", return_value=5.0),
        patch.object(SBOMService, "generate", return_value=MagicMock()),
        patch.object(QualityGateService, "create", return_value=MagicMock()),
        patch.object(QualityGateService, "evaluate"),
        patch.object(AuditDao, "create", return_value=False) as mock_dao_create,
    ):
        # WHEN
        audit = AuditService().run_audit(project, "global")

        # THEN
        assert audit is None
        mock_dao_create.assert_called_once()
