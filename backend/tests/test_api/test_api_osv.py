from unittest.mock import MagicMock, patch

import pytest
import requests

from api_osv.api_osv import API_OSV
from business_object.dependency import Dependency
from business_object.vulnerability.critical_vulnerability import CriticalVulnerability
from business_object.vulnerability.high_vulnerability import HighVulnerability
from business_object.vulnerability.low_vulnerability import LowVulnerability
from business_object.vulnerability.medium_vulnerability import MediumVulnerability

MODULE = "api_osv.api_osv"

CRITICAL_VECTOR = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"  # 9.8
HIGH_VECTOR = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"  # 7.5
MEDIUM_VECTOR = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"  # 5.3
ZERO_VECTOR = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N"  # 0.0
CVSS2_HIGH = "AV:N/AC:L/Au:N/C:P/I:P/A:P"  # 7.5
CVSS4_CRITICAL = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"  # 9.3


def fake_cvss(score: float) -> MagicMock:
    """Fake CVSS class whose instances always return the given score."""
    cls = MagicMock()
    cls.return_value.scores.return_value = (score,)
    return cls


def osv_entry(osv_id: str, vector: str | None = None, aliases=None) -> dict:
    entry = {"id": osv_id, "aliases": aliases or []}
    if vector:
        entry["severity"] = [{"type": "CVSS_V3", "score": vector}]
    return entry


def mock_post(data: dict) -> MagicMock:
    response = MagicMock()
    response.json.return_value = data
    return MagicMock(return_value=response)


class TestGetSeverity:
    @pytest.mark.parametrize(
        "vector, expected",
        [
            (CRITICAL_VECTOR, "CRITICAL"),
            (HIGH_VECTOR, "HIGH"),
            (MEDIUM_VECTOR, "MEDIUM"),
            (ZERO_VECTOR, None),
        ],
    )
    def test_severity_mapping(self, vector, expected):
        vuln = {"severity": [{"type": "CVSS_V3", "score": vector}]}
        assert API_OSV._get_severity(vuln) == expected

    @pytest.mark.parametrize(
        "score, expected",
        [
            (0.1, "LOW"),
            (3.9, "LOW"),
            (4.0, "MEDIUM"),
            (6.9, "MEDIUM"),
            (7.0, "HIGH"),
            (8.9, "HIGH"),
            (9.0, "CRITICAL"),
            (10.0, "CRITICAL"),
        ],
    )
    def test_threshold_boundaries(self, score, expected):
        vuln = {"severity": [{"type": "CVSS_V3", "score": "vector"}]}
        with patch(f"{MODULE}.CVSS3", fake_cvss(score)):
            assert API_OSV._get_severity(vuln) == expected

    @pytest.mark.parametrize(
        "cvss_type, cls_name",
        [
            ("CVSS_V2", "CVSS2"),
            ("CVSS_V3", "CVSS3"),
            ("CVSS_V4", "CVSS4"),
        ],
    )
    def test_each_cvss_version_uses_its_parser(self, cvss_type, cls_name):
        vuln = {"severity": [{"type": cvss_type, "score": "vector"}]}
        with patch(f"{MODULE}.{cls_name}", fake_cvss(8.0)) as parser:
            assert API_OSV._get_severity(vuln) == "HIGH"
            parser.assert_called_once_with("vector")

    def test_skips_unknown_cvss_type(self):
        vuln = {"severity": [{"type": "CVSS_V5", "score": "CVSS:5.0/..."}]}
        assert API_OSV._get_severity(vuln) is None

    def test_missing_severity_list(self):
        assert API_OSV._get_severity({}) is None

    def test_invalid_vector_returns_none(self):
        vuln = {"severity": [{"type": "CVSS_V3", "score": "pas-un-vecteur"}]}
        assert API_OSV._get_severity(vuln) is None

    def test_invalid_vector_then_valid_one(self):
        """An unparsable entry is skipped, the next one is used."""
        vuln = {
            "severity": [
                {"type": "CVSS_V3", "score": "pas-un-vecteur"},
                {"type": "CVSS_V3", "score": CRITICAL_VECTOR},
            ]
        }
        assert API_OSV._get_severity(vuln) == "CRITICAL"

    def test_real_cvss2_vector(self):
        vuln = {"severity": [{"type": "CVSS_V2", "score": CVSS2_HIGH}]}
        assert API_OSV._get_severity(vuln) == "HIGH"

    def test_real_cvss4_vector(self):
        vuln = {"severity": [{"type": "CVSS_V4", "score": CVSS4_CRITICAL}]}
        assert API_OSV._get_severity(vuln) == "CRITICAL"

    def test_first_readable_entry_wins(self):
        vuln = {
            "severity": [
                {"type": "CVSS_V3", "score": MEDIUM_VECTOR},
                {"type": "CVSS_V2", "score": CVSS2_HIGH},
            ]
        }
        assert API_OSV._get_severity(vuln) == "MEDIUM"


class TestToVulnerability:
    @pytest.mark.parametrize(
        "severity, expected_class",
        [
            ("LOW", LowVulnerability),
            ("MEDIUM", MediumVulnerability),
            ("HIGH", HighVulnerability),
            ("CRITICAL", CriticalVulnerability),
        ],
    )
    def test_creates_correct_vulnerability_class(self, severity, expected_class):
        osv_vuln = {"id": "GHSA-1234", "aliases": ["CVE-2024-1234"]}
        dep = Dependency(id_dependency=1, name="requests", version="2.19.0")
        assert isinstance(API_OSV._to_vulnerability(osv_vuln, dep, severity), expected_class)

    def test_sets_correct_fields(self):
        osv_vuln = {"id": "GHSA-XXXX", "aliases": ["CVE-2024-5678"]}
        dep = Dependency(id_dependency=1, name="express", version="4.17.1")
        vuln = API_OSV._to_vulnerability(osv_vuln, dep, "MEDIUM")

        assert vuln.osv_id == "GHSA-XXXX"
        assert vuln.cve_id == "CVE-2024-5678"
        assert vuln.package == "express"
        assert vuln.version_package == "4.17.1"
        assert vuln.id_vulnerability is None

    def test_handles_missing_cve(self):
        osv_vuln = {"id": "PYSEC-2024-99", "aliases": []}
        dep = Dependency(id_dependency=1, name="flask", version="2.0.0")
        vuln = API_OSV._to_vulnerability(osv_vuln, dep, "HIGH")
        assert vuln.cve_id is None

    def test_takes_first_cve_among_aliases(self):
        osv_vuln = {"id": "GHSA-1", "aliases": ["GHSA-2", "CVE-2024-1", "CVE-2024-2"]}
        vuln = API_OSV._to_vulnerability(
            osv_vuln, Dependency(id_dependency=1, name="x", version="1.0"), "LOW"
        )
        assert vuln.cve_id == "CVE-2024-1"

    def test_missing_aliases_key(self):
        vuln = API_OSV._to_vulnerability(
            {"id": "GHSA-1"}, Dependency(id_dependency=1, name="x", version="1.0"), "LOW"
        )
        assert vuln.cve_id is None


class TestFindVulnerabilities:
    dep = Dependency(id_dependency=1, name="requests", version="2.19.0")

    def test_success_with_multiple_vulns(self):
        data = {
            "vulns": [
                osv_entry("GHSA-1", CRITICAL_VECTOR, ["CVE-2024-1"]),
                osv_entry("GHSA-2", MEDIUM_VECTOR),
            ]
        }
        with patch(f"{MODULE}.requests.post", mock_post(data)):
            result = API_OSV.find_vulnerabilities(self.dep, "PyPI")

        assert len(result) == 2
        assert isinstance(result[0], CriticalVulnerability)
        assert isinstance(result[1], MediumVulnerability)
        assert result[0].cve_id == "CVE-2024-1"
        assert all(v.package == "requests" for v in result)

    def test_no_vulnerabilities(self):
        with patch(f"{MODULE}.requests.post", mock_post({})):
            assert API_OSV.find_vulnerabilities(self.dep, "PyPI") == []

    def test_vuln_without_severity_is_skipped(self):
        data = {"vulns": [osv_entry("GHSA-1"), osv_entry("GHSA-2", HIGH_VECTOR)]}
        with patch(f"{MODULE}.requests.post", mock_post(data)):
            result = API_OSV.find_vulnerabilities(self.dep, "PyPI")
        assert [v.osv_id for v in result] == ["GHSA-2"]

    def test_sends_correct_request(self):
        post = mock_post({})
        with patch(f"{MODULE}.requests.post", post):
            API_OSV.find_vulnerabilities(self.dep, "PyPI")

        post.assert_called_once_with(
            API_OSV.BASE_URL,
            json={"package": {"name": "requests", "ecosystem": "PyPI"}, "version": "2.19.0"},
            timeout=10,
        )

    def test_http_error_is_propagated(self):
        response = MagicMock()
        response.raise_for_status.side_effect = requests.HTTPError("500")
        with patch(f"{MODULE}.requests.post", MagicMock(return_value=response)):
            with pytest.raises(requests.HTTPError):
                API_OSV.find_vulnerabilities(self.dep, "PyPI")

    def test_timeout_is_propagated(self):
        with patch(f"{MODULE}.requests.post", MagicMock(side_effect=requests.Timeout)):
            with pytest.raises(requests.Timeout):
                API_OSV.find_vulnerabilities(self.dep, "PyPI")

    def test_version_none_is_sent_as_null(self):
        post = mock_post({})
        dep = Dependency(id_dependency=1, name="requests", version=None)
        with patch(f"{MODULE}.requests.post", post):
            API_OSV.find_vulnerabilities(dep, "PyPI")
        assert post.call_args.kwargs["json"]["version"] is None

    def test_invalid_json_is_propagated(self):
        response = MagicMock()
        response.json.side_effect = ValueError("not json")
        with patch(f"{MODULE}.requests.post", MagicMock(return_value=response)):
            with pytest.raises(ValueError):
                API_OSV.find_vulnerabilities(self.dep, "PyPI")
