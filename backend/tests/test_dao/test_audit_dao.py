from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from business_object.audit import Audit
from business_object.qualitygate.qualitygate import QualityGate
from business_object.vulnerability.critical_vulnerability import (
    CriticalVulnerability,
)
from business_object.vulnerability.high_vulnerability import HighVulnerability
from dao.audit_dao import AuditDao
from service.qualitygate_service import QualityGateService


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
        # Audit expects a QualityGate object, not a status string.
        quality_gate=QualityGateService().create("global", 5, 0, 1, 0.001, "PASSED"),
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
        "type_qualitygate": "global",
        "status_qualitygate": "passed",
        "certificate_pdf": None,
        "certificate_signed": None,
        "certificate_id": 1,
        "sbom_content": None,
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

    # The DAO reconstructs a QualityGate domain object from the DB columns.
    assert isinstance(result.quality_gate, QualityGate)
    assert result.quality_gate.get_type() == "global"
    assert result.quality_gate.status == "passed"

    assert result.vulnerabilities == []
    assert result.licenses == []
    assert result.anti_patterns == []
    # The current DAO creates an empty SBOM when sbom_content is NULL.
    assert result.sbom is not None
    assert result.certificate is None


def test_row_to_audit_with_json_string_certificate():
    """Decode certificate_signed when the DB driver returns JSON as text."""
    signed_data = {
        "payload": {
            "issued_at": "2026-10-25T09:30:00",
            "cert_id": "certificate-5",
        }
    }
    import json

    row = db_row(
        certificate_signed=json.dumps(signed_data),
        certificate_pdf=b"%PDF-test",
    )

    result = AuditDao._row_to_audit(row)

    assert result.certificate is not None
    assert result.certificate.signed_data == signed_data


def test_row_to_audit_with_sbom_content():
    """Rebuild the SBOM file when sbom_content is stored."""
    row = db_row(sbom_content=b'{"bomFormat": "CycloneDX"}')

    result = AuditDao._row_to_audit(row)

    assert result.sbom.content == b'{"bomFormat": "CycloneDX"}'
    assert result.sbom.name == "sbom_5.json"


# -------------------- _get_quality_gate_data --------------------


def test_get_quality_gate_data_none():
    """Return no type and no status when there is no quality gate."""
    assert AuditDao._get_quality_gate_data(None) == (None, None)


def test_get_quality_gate_data_string():
    """A plain string is used as the status, without type."""
    assert AuditDao._get_quality_gate_data("PASSED") == (None, "PASSED")


def test_get_quality_gate_data_object(audit):
    """Return the type and the status of a QualityGate object."""
    assert AuditDao._get_quality_gate_data(audit.quality_gate) == ("global", "PASSED")


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
    assert params["complexity"] == 12.5
    assert params["energy_comsumption"] == 2.5
    assert params["carbon_emission_gco2e"] == 1.2
    assert params["type_qualitygate"] == "global"
    assert params["status_qualitygate"] == "PASSED"
    assert "sbom_content" in params


def test_create_quality_gate_object(dao, audit, mock_db):
    """Persist the type and status exposed by a QualityGate object."""
    db, cursor = mock_db
    cursor.fetchone.return_value = {
        "id_audit": 42,
        "date": audit.date,
    }
    audit.quality_gate = MagicMock()
    audit.quality_gate.get_type.return_value = "security"
    audit.quality_gate.status = "FAILED"

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.create(audit)

    assert result is True
    params = cursor.execute.call_args.args[1]
    assert params["type_qualitygate"] == "security"
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
    assert params["type_qualitygate"] == "global"
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
    """Create an audit when its vulnerabilities collection is None."""
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
    # Vulnerability totals are not columns in the current audit_table schema.
    assert "total_vulnerability" not in params
    assert "total_critical_vulnerability" not in params


# -------------------- list_all_audit --------------------


def test_list_all_audit_success(dao, mock_db):
    """Return the audits of the given project."""
    db, cursor = mock_db
    cursor.fetchall.return_value = [
        db_row(id_audit=1),
        db_row(id_audit=2, status_qualitygate="FAILED"),
    ]
    project = MagicMock(id_project=12)

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.list_all_audit(project)

    assert len(result) == 2
    assert all(isinstance(item, Audit) for item in result)
    assert [item.id_audit for item in result] == [1, 2]
    assert cursor.execute.call_args.args[1] == {"id_project": 12}


def test_list_all_audit_empty(dao, mock_db):
    """Return an empty list when the project has no audit."""
    db, cursor = mock_db
    cursor.fetchall.return_value = []

    with patch("dao.audit_dao.DBConnection", return_value=db):
        result = dao.list_all_audit(MagicMock(id_project=12))

    assert result == []


def test_list_all_audit_database_error_is_reraised(dao):
    """Re-raise database errors."""
    with patch(
        "dao.audit_dao.DBConnection",
        side_effect=RuntimeError("db down"),
    ):
        with pytest.raises(RuntimeError, match="db down"):
            dao.list_all_audit(MagicMock(id_project=12))
