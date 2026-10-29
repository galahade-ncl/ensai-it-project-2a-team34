import datetime
from unittest.mock import MagicMock

from business_object.audit import Audit
from dao.audit_dao import AuditDao
from service.audit_service import AuditService


def test_create_successful():
    """Successfully create an Audit"""

    # GIVEN
    id_audit, id_project = 1, 10
    date = datetime.datetime(2025, 1, 15)
    vulnerabilities, licenses, anti_patterns, certificate = [], [], [], []
    complexity, energy_consumption_kwh, carbon_emission_gco2e = 4.2, 0.35, 12.5
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
    vulnerabilities, licenses, anti_patterns, certificate = [], [], [], []
    complexity, energy_consumption_kwh, carbon_emission_gco2e = 4.2, 0.35, 12.5
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