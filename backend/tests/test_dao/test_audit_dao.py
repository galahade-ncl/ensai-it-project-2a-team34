from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from business_object.audit import Audit
from business_object.vulnerability.critical_vulnerability import (
    CriticalVulnerability,
)
from business_object.vulnerability.high_vulnerability import (
    HighVulnerability,
)
from dao.audit_dao import AuditDao


@pytest.fixture
def audit():
    """Create a sample audit containing two critical vulnerabilities."""
    return Audit(
        id_audit=7,
        id_project=12,
        date=datetime(2026, 10, 25, 10, 0),
        vulnerabilities=[
            CriticalVulnerability(1, "OSV-1", None, "package-a", "1.0"),
            HighVulnerability(2, "OSV-2", None, "package-b", "2.0"),
            CriticalVulnerability(3, "OSV-3", None, "package-c", "3.0"),
        ],
        licenses=[],
        anti_patterns=[],
        complexity=12.5,
        energy_consumption_kwh=2.5,
        carbon_emission_gco2e=1.2,
        sbom=None,
        quality_gate="PASSED",
        certificate=None,
    )


@pytest.fixture
def mock_db():
    """Create a mocked database connection and cursor."""
    db = MagicMock()
    connection = db.connection.__enter__.return_value
    cursor = connection.cursor.return_value.__enter__.return_value
    return db, cursor


@pytest.fixture
def dao():
    """Create an AuditDao instance."""
    return AuditDao()


def db_row(**overrides):
    """Create a sample database row."""
    row = {
        "id_audit": 5,
        "id_project": 12,
        "date": datetime(2026, 10, 25, 9, 30),
        "complexity": 15.0,
        "energy_comsumption": 3.5,
        "carbon_emission_gco2e": 2.1,
        "status_qualitygate": "PASSED",
        "total_vulnerability": 3,
        "total_critical_vulnerability": 2,
    }
    row.update(overrides)
    return row


# -------------------- _row_to_audit --------------------


def test_row_to_audit():
    """Convert a database row into an Audit object."""
    row = db_row()

    result = AuditDao._row_to_audit(row)

    assert isinstance(result, Audit)
    assert result.id_audit == 5
    assert result.id_project == 12
    assert result.date == row["date"]
    assert result.complexity == 15.0
    assert result.energy_consumption_kwh == 3.5
    assert result.carbon_emission_gco2e == 2.1
    assert result.quality_gate == "PASSED"
    assert result.vulnerabilities == []
    assert result.licenses == []
    assert result.anti_patterns == []
    assert result.sbom is None
    assert result.certificate is None


# -------------------- create --------------------


def test_create_success(dao, audit, mock_db):
    """Create an audit successfully."""
    db, cursor = mock_db
    generated_date = datetime(2026, 10, 25, 11, 0)

    cursor.fetchone.return_value = {
        "id_audit": 42,
        "date": generated_date,
    }

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.create(audit)

    assert result is True
    assert audit.id_audit == 42
    assert audit.date == generated_date

    params = cursor.execute.call_args.args[1]

    assert params["id_project"] == 12
    assert params["total_vulnerability"] == 3
    assert params["total_critical_vulnerability"] == 2
    assert params["complexity"] == 12.5
    assert params["energy_comsumption"] == 2.5
    assert params["carbon_emission_gco2e"] == 1.2
    assert params["status_qualitygate"] == "PASSED"


def test_create_quality_gate_object(dao, audit, mock_db):
    """Read the status from a quality gate object."""
    db, cursor = mock_db
    cursor.fetchone.return_value = {
        "id_audit": 42,
        "date": audit.date,
    }
    audit.quality_gate = MagicMock(status="FAILED")

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.create(audit)

    assert result is True
    params = cursor.execute.call_args.args[1]
    assert params["status_qualitygate"] == "FAILED"


def test_create_without_returned_row(dao, audit, mock_db):
    """Return False if INSERT returns no row."""
    db, cursor = mock_db
    cursor.fetchone.return_value = None

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.create(audit)

    assert result is False


def test_create_database_error_is_reraised(dao, audit):
    """Re-raise database errors."""
    with patch(
        "dao.audit_dao.DBConnection",
        side_effect=RuntimeError("db down"),
    ):
        with pytest.raises(RuntimeError, match="db down"):
            dao.create(audit)


# -------------------- find_by_id --------------------


def test_find_by_id_success(dao, mock_db):
    """Return an audit when its ID exists."""
    db, cursor = mock_db
    cursor.fetchone.return_value = db_row()

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.find_by_id(5)

    assert isinstance(result, Audit)
    assert result.id_audit == 5
    assert result.id_project == 12
    assert cursor.execute.call_args.args[1] == {"id_audit": 5}


def test_find_by_id_not_found(dao, mock_db):
    """Return None when the audit does not exist."""
    db, cursor = mock_db
    cursor.fetchone.return_value = None

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.find_by_id(999)

    assert result is None


def test_find_by_id_database_error_is_reraised(dao):
    """Re-raise database errors."""
    with patch(
        "dao.audit_dao.DBConnection",
        side_effect=RuntimeError("db down"),
    ):
        with pytest.raises(RuntimeError, match="db down"):
            dao.find_by_id(5)


# -------------------- find_all --------------------


def test_find_all_success(dao, mock_db):
    """Return all audits from the database."""
    db, cursor = mock_db
    cursor.fetchall.return_value = [
        db_row(id_audit=1),
        db_row(id_audit=2, status_qualitygate="FAILED"),
    ]

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.find_all()

    assert len(result) == 2
    assert all(isinstance(item, Audit) for item in result)
    assert [item.id_audit for item in result] == [1, 2]


def test_find_all_empty(dao, mock_db):
    """Return an empty list when there are no audits."""
    db, cursor = mock_db
    cursor.fetchall.return_value = []

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.find_all()

    assert result == []


def test_find_all_database_error_is_reraised(dao):
    """Re-raise database errors."""
    with patch(
        "dao.audit_dao.DBConnection",
        side_effect=RuntimeError("db down"),
    ):
        with pytest.raises(RuntimeError, match="db down"):
            dao.find_all()


# -------------------- update --------------------


def test_update_success(dao, audit, mock_db):
    """Return True when one audit is updated."""
    db, cursor = mock_db
    cursor.rowcount = 1

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.update(audit)

    assert result is True

    params = cursor.execute.call_args.args[1]

    assert params["id_audit"] == 7
    assert params["id_project"] == 12
    assert params["total_vulnerability"] == 3
    assert params["total_critical_vulnerability"] == 2
    assert params["status_qualitygate"] == "PASSED"


def test_update_not_found(dao, audit, mock_db):
    """Return False when no audit is updated."""
    db, cursor = mock_db
    cursor.rowcount = 0

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.update(audit)

    assert result is False


def test_update_database_error_is_reraised(dao, audit):
    """Re-raise database errors."""
    with patch(
        "dao.audit_dao.DBConnection",
        side_effect=RuntimeError("db down"),
    ):
        with pytest.raises(RuntimeError, match="db down"):
            dao.update(audit)


# -------------------- delete --------------------


def test_delete_success(dao, audit, mock_db):
    """Return True when an audit is deleted."""
    db, cursor = mock_db
    cursor.rowcount = 1

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.delete(audit)

    assert result is True
    assert cursor.execute.call_args.args[1] == {"id_audit": 7}


def test_delete_not_found(dao, audit, mock_db):
    """Return False when no audit is deleted."""
    db, cursor = mock_db
    cursor.rowcount = 0

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.delete(audit)

    assert result is False


def test_delete_database_error_is_reraised(dao, audit):
    """Re-raise database errors."""
    with patch(
        "dao.audit_dao.DBConnection",
        side_effect=RuntimeError("db down"),
    ):
        with pytest.raises(RuntimeError, match="db down"):
            dao.delete(audit)


def test_create_with_none_vulnerabilities(dao, audit, mock_db):
    """Create an audit when vulnerabilities is None."""
    db, cursor = mock_db

    cursor.fetchone.return_value = {
        "id_audit": 42,
        "date": audit.date,
    }

    audit.vulnerabilities = None

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.create(audit)

    assert result is True

    params = cursor.execute.call_args.args[1]

    assert params["total_vulnerability"] == 0
    assert params["total_critical_vulnerability"] == 0
