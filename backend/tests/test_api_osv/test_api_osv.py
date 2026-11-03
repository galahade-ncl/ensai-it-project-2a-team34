from unittest.mock import MagicMock

import pytest
from src.api_osv.api_osv import API_OSV
from src.business_object.dependency import Dependency

from business_object.vulnerability.critical_vulnerability import CriticalVulnerability
from business_object.vulnerability.high_vulnerability import HighVulnerability
from business_object.vulnerability.low_vulnerability import LowVulnerability
from business_object.vulnerability.medium_vulnerability import MediumVulnerability

MODULE = "api.api_osv"  # le chemin du fichier où est API_OSV


def fake_cvss(score: float) -> MagicMock:
    """Fake CVSS class whose instances always return the given score."""
    cls = MagicMock()
    cls.return_value.scores.return_value = (score,)
    return cls


class TestGetSeverity:
    """Teste la détermination de la sévérité depuis les vecteurs CVSS."""

    @pytest.mark.parametrize(
        "cvss_vector, expected",
        [
            ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", "CRITICAL"),  # 9.8
            ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H", "HIGH"),  # 7.5
            ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L", "MEDIUM"),  # 5.3
            (
                "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N",
                None,
            ),  # 0.0
        ],
    )
    def test_severity_mapping(self, cvss_vector, expected):
        vuln = {"severity": [{"type": "CVSS_V3", "score": cvss_vector}]}
        assert API_OSV._get_severity(vuln) == expected

    # def test_returns_none_for_zero_score(self):
    #     vuln = {
    #         "severity": [
    #             {"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N"}
    #         ]
    #     }
    #     assert API_OSV._get_severity(vuln) is None

    def test_skips_unknown_cvss_type(self):
        vuln = {"severity": [{"type": "CVSS_V5", "score": "CVSS:5.0/..."}]}
        assert API_OSV._get_severity(vuln) is None

    def test_missing_severity_list(self):
        assert API_OSV._get_severity({}) is None

    #     @pytest.mark.parametrize(
    #     "score, expected",
    #     [
    #         (3.9, "LOW"), (4.0, "MEDIUM"),
    #         (6.9, "MEDIUM"), (7.0, "HIGH"),
    #         (8.9, "HIGH"), (9.0, "CRITICAL"),
    #     ],
    # )
    # def test_threshold_boundaries(self, score, expected):
    #     """Check the exact limits between two severity levels."""
    #     vuln = {"severity": [{"type": "CVSS_V3", "score": "vector"}]}
    #     with patch(f"{MODULE}.CVSS3", fake_cvss(score)):
    #         assert API_OSV._get_severity(vuln) == expected

    # def test_invalid_vector_returns_none(self):
    #     """Return None when the CVSS vector cannot be parsed."""
    #     vuln = {"severity": [{"type": "CVSS_V3", "score": "pas-un-vecteur"}]}
    #     assert API_OSV._get_severity(vuln) is None


class TestToVulnerability:
    """Test the conversion of the API dictionary into a business object."""

    def test_creates_correct_vulnerability_class(self):
        osv_vuln = {"id": "GHSA-1234", "aliases": ["CVE-2024-1234"]}
        dep = Dependency(1, "requests", "2.19.0")

        assert isinstance(API_OSV._to_vulnerability(osv_vuln, dep, "MEDIUM"), MediumVulnerability)
        assert isinstance(API_OSV._to_vulnerability(osv_vuln, dep, "HIGH"), HighVulnerability)
        assert isinstance(API_OSV._to_vulnerability(osv_vuln, dep, "LOW"), LowVulnerability)
        assert isinstance(
            API_OSV._to_vulnerability(osv_vuln, dep, "CRITICAL"), CriticalVulnerability
        )

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
        dep = Dependency(1, "flask", "2.0.0")
        vuln = API_OSV._to_vulnerability(osv_vuln, dep, "HIGH")
        assert vuln.cve_id is None


# class TestFindVulnerabilities:
#     """Teste le flux complet avec mock de l'API externe."""

#     def test_success_with_multiple_vulns(self):
#         mock_response_data = {
#             "vulns": [
#                 {"id": "GHSA-1", "aliases":
