import base64
import hashlib
import json
import uuid
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from business_object.audit import Audit
from business_object.file.certificatefile import CertificateFile
from business_object.file.codefile import CodeFile
from business_object.file.dependencyfile import DependencyFile
from business_object.project import Project
from service.certificate_service import CertificateService
from utils.security import get_key_id, load_signing_key

"""
Tests for CertificateService.generate_certificate(), sign_certificate(),
verify_certificate() and CertificateFile.get_duty()
The signing key is read from CERT_SIGNING_PRIVATE_KEY and cached by
utils.security.load_signing_key (lru_cache), so every test installs a
throw-away key pair and clears that cache before and after running.
"""

# --------------------------------------------------------------- HELPERS
def make_pem(key: Ed25519PrivateKey | None = None) -> str:
    """Return a private Ed25519 key in PEM format."""
    key = key or Ed25519PrivateKey.generate()
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()


def make_audit(status="Passed", vulnerabilities=None) -> Audit:
    """Audit carrying only what the certificate payload reads.

    The quality gate is a stand-in object: generate_certificate() only
    reads its status.
    """
    return Audit(
        id_audit=42,
        id_project=1,
        date=datetime(2026, 11, 19, 14, 35, 27),
        vulnerabilities=[] if vulnerabilities is None else vulnerabilities,
        licenses=[],
        anti_patterns=[],
        complexity=1.0,
        energy_consumption_kwh=0.000123456789,
        carbon_emission_gco2e=0.0061728,
        sbom=None,
        quality_gate=SimpleNamespace(status=status),
        certificate=None,
    )


def make_project(name_project="demo") -> Project:
    """Project holding the two files whose hashes go into the payload."""
    return Project(
        name_project=name_project,
        secretHMACkey=bytes(32),
        id_project=1,
        codefile=CodeFile(name="main", content=b"print('hello')", type_file="py"),
        dependencyfile=DependencyFile(
            name="requirements", content=b"requests==2.31.0", type_file="txt"
        ),
    )


# ----------------------------------------- FIXTURES
@pytest.fixture(autouse=True)
def signing_key(monkeypatch):
    """Install a throw-away signing key and reset the cache around each test."""
    monkeypatch.setenv("CERT_SIGNING_PRIVATE_KEY", make_pem())
    load_signing_key.cache_clear()
    yield
    load_signing_key.cache_clear()


@pytest.fixture
def audit():
    return make_audit()


@pytest.fixture
def project():
    return make_project()


# -------------------------------------------- CertificateFile.get_duty()
def test_certificatefile_get_duty():
    certificate = CertificateFile(
        name="Certificate: global",
        content=b"%PDF-1.4",
        type_file="pdf",
        qualitygate_type="global",
        date=None,
        signed_data={},
    )
    assert certificate.get_duty() == "certificate"


# ------------------------------------------------- generate_certificate()
def test_generate_certificate_successful(audit, project):
    certificate = CertificateService().generate_certificate(audit, project, "global")

    assert isinstance(certificate, CertificateFile)
    assert certificate.name == "Certificate: global"
    assert certificate.type_file == "pdf"
    assert certificate.qualitygate_type == "global"
    assert certificate.date == datetime.now(UTC).date().isoformat()
    # a real PDF document, not an empty placeholder
    assert certificate.content.startswith(b"%PDF")
    assert b"%%EOF" in certificate.content


@pytest.mark.parametrize("qualitygate_type", ["eco", "security", "global"])
def test_generate_certificate_for_every_qualitygate(audit, project, qualitygate_type):
    certificate = CertificateService().generate_certificate(audit, project, qualitygate_type)

    assert certificate.name == f"Certificate: {qualitygate_type}"
    assert certificate.signed_data["payload"]["qualitygate_type"] == qualitygate_type


def test_generate_certificate_unknown_qualitygate(audit, project):
    with pytest.raises(ValueError):
        CertificateService().generate_certificate(audit, project, "unknown")


def test_generate_certificate_payload(audit, project):
    payload = CertificateService().generate_certificate(audit, project, "eco").signed_data[
        "payload"
    ]

    uuid.UUID(payload["cert_id"])  # raises if the identifier is not a UUID
    assert payload["audit_id"] == 42
    assert payload["project_id"] == 1
    assert payload["project_name"] == "demo"
    assert payload["qualitygate_status"] == "Passed"
    assert payload["app_version"] == "1.0.0"

    # the date is timezone-aware, so two certificates can always be compared
    assert datetime.fromisoformat(payload["issued_at"]).tzinfo is not None

    # the payload binds the certificate to the exact files that were audited
    assert payload["files"]["code_sha256"] == hashlib.sha256(b"print('hello')").hexdigest()
    assert (
        payload["files"]["dependencies_sha256"]
        == hashlib.sha256(b"requests==2.31.0").hexdigest()
    )

    # figures are frozen as strings, rounded to six decimals
    assert payload["summary"]["vulnerabilities"] == 0
    assert payload["summary"]["energy_consumption_kwh"] == "0.000123"
    assert payload["summary"]["carbon_emission_gco2e"] == "0.006173"


def test_generate_certificate_counts_vulnerabilities(project):
    audit = make_audit(vulnerabilities=["first", "second", "third"])
    payload = CertificateService().generate_certificate(audit, project, "security").signed_data[
        "payload"
    ]
    assert payload["summary"]["vulnerabilities"] == 3


def test_generate_certificate_ids_are_unique(audit, project):
    first = CertificateService().generate_certificate(audit, project, "global")
    second = CertificateService().generate_certificate(audit, project, "global")
    assert first.signed_data["payload"]["cert_id"] != second.signed_data["payload"]["cert_id"]


def test_generate_certificate_signed_data_is_json_serializable(audit, project):
    """The QR code embeds this dictionary, so it has to be serializable."""
    certificate = CertificateService().generate_certificate(audit, project, "global")
    assert json.loads(json.dumps(certificate.signed_data)) == certificate.signed_data


def test_generate_certificate_is_self_verifiable(audit, project):
    certificate = CertificateService().generate_certificate(audit, project, "global")
    assert CertificateService().verify_certificate(certificate.signed_data) is True


# -------------------------- sign_certificate()
def test_sign_certificate_structure():
    signed = CertificateService().sign_certificate({"cert_id": "abc"})

    assert set(signed) == {"payload", "kid", "alg", "signature"}
    assert signed["payload"] == {"cert_id": "abc"}
    assert signed["alg"] == "Ed25519"
    assert signed["kid"] == get_key_id()
    assert len(base64.b64decode(signed["signature"])) == 64  # Ed25519 signature size


def test_sign_certificate_is_deterministic():
    """Ed25519 is deterministic: the same payload always gives the same signature."""
    payload = {"cert_id": "abc", "project_name": "demo"}
    first = CertificateService().sign_certificate(payload)
    second = CertificateService().sign_certificate(payload)
    assert first["signature"] == second["signature"]


def test_sign_certificate_ignores_key_order():
    """canonical_json sorts the keys, so insertion order must not matter."""
    first = CertificateService().sign_certificate({"a": 1, "b": 2})
    second = CertificateService().sign_certificate({"b": 2, "a": 1})
    assert first["signature"] == second["signature"]


def test_sign_certificate_without_key(monkeypatch):
    monkeypatch.delenv("CERT_SIGNING_PRIVATE_KEY", raising=False)
    load_signing_key.cache_clear()
    with pytest.raises(RuntimeError):
        CertificateService().sign_certificate({"cert_id": "abc"})


def test_sign_certificate_accepts_a_single_line_pem(monkeypatch):
    """generate_signing_key.py prints the PEM with escaped newlines."""
    monkeypatch.setenv("CERT_SIGNING_PRIVATE_KEY", make_pem().strip().replace("\n", "\\n"))
    load_signing_key.cache_clear()

    signed = CertificateService().sign_certificate({"cert_id": "abc"})
    assert CertificateService().verify_certificate(signed) is True


# -------------------------- verify_certificate()
def test_verify_certificate_successful():
    signed = CertificateService().sign_certificate({"cert_id": "abc"})
    assert CertificateService().verify_certificate(signed) is True


def test_verify_certificate_rejects_modified_payload():
    signed = CertificateService().sign_certificate({"cert_id": "abc", "project_name": "demo"})
    signed["payload"]["project_name"] = "tampered"
    assert CertificateService().verify_certificate(signed) is False


def test_verify_certificate_rejects_modified_signature():
    signed = CertificateService().sign_certificate({"cert_id": "abc"})
    signed["signature"] = base64.b64encode(bytes(64)).decode("ascii")
    assert CertificateService().verify_certificate(signed) is False


def test_verify_certificate_rejects_another_key(monkeypatch):
    """A certificate signed with another key pair must not pass."""
    signed = CertificateService().sign_certificate({"cert_id": "abc"})

    monkeypatch.setenv("CERT_SIGNING_PRIVATE_KEY", make_pem())
    load_signing_key.cache_clear()

    assert signed["kid"] != get_key_id()
    assert CertificateService().verify_certificate(signed) is False


@pytest.mark.parametrize(
    "certificate",
    [
        {},
        {"kid": "0000000000000000", "alg": "Ed25519", "signature": "AAAA", "payload": {}},
        {"payload": {}, "alg": "Ed25519", "signature": "AAAA"},
    ],
    ids=["empty", "unknown kid", "missing kid"],
)
def test_verify_certificate_rejects_malformed_input(certificate):
    assert CertificateService().verify_certificate(certificate) is False


def test_verify_certificate_rejects_invalid_base64():
    signed = CertificateService().sign_certificate({"cert_id": "abc"})
    signed["signature"] = "not base64 at all !!"
    assert CertificateService().verify_certificate(signed) is False
