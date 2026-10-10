import requests
from critical_vulnerability import CriticalVulnerability
from cvss import CVSS2, CVSS3, CVSS4
from dependency import Dependency
from high_vulnerability import HighVulnerability
from low_vulnerability import LowVulnerability
from medium_vulnerability import MediumVulnerability
from vulnerability import Vulnerability

from utils.log_utils import log


class API_OSV:
    """
    Class that handles all the calls of the external API OSV
    """

    BASE_URL = "https://api.osv.dev/v1/query"

    @staticmethod
    @log
    def find_vulnerabilities(dependency: Dependency, ecosystem: str) -> list[Vulnerability]:
        """
        Methode that find all the vulnerabilities linked to a dependency
        Args:
            dependency (Dependency) : the dependency to analyse in the external api
            ecosystem (str) : the ecosystem associated with the dependencyfile
        Returns:
            list[Vulnerability]
        """
        payload = {
            "package": {
                "name": dependency.name,
                "ecosystem": ecosystem,
            },
            "version": dependency.version,
        }

        response = requests.post(
            API_OSV.BASE_URL,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()

        vulnerabilities = []

        for osv_vuln in data.get("vulns", []):
            severity = API_OSV._get_severity(osv_vuln)

            if severity is None:
                continue

            vulnerability = API_OSV._to_vulnerability(
                osv_vuln,
                dependency,
                severity,
            )
            vulnerabilities.append(vulnerability)

        return vulnerabilities

    @staticmethod
    def _get_severity(osv_vuln: dict) -> str | None:
        """
        Determine severity from a CVSS vector
        Args:
            osv_vuln (dict) : the dependency to analyse in the external api
        Returns:
            A string object corresponding to the severity or None if there isn't a risk from the vulnerability
        """

        for item in osv_vuln.get("severity", []):
            vector = item.get("score", "")
            cvss_type = item.get("type", "")

            try:
                if cvss_type == "CVSS_V4":
                    score = CVSS4(vector).scores()[0]
                elif cvss_type == "CVSS_V3":
                    score = CVSS3(vector).scores()[0]
                elif cvss_type == "CVSS_V2":
                    score = CVSS2(vector).scores()[0]
                else:
                    continue

                if score == 0:
                    return None
                if score < 4:
                    return "LOW"
                if score < 7:
                    return "MEDIUM"
                if score < 9:
                    return "HIGH"
                return "CRITICAL"

            except (ValueError, TypeError, IndexError):
                continue

        return None

    @staticmethod
    def _to_vulnerability(osv_vuln: dict, dependency: Dependency, severity: str) -> Vulnerability:
        """
        Transform the response of the API to a Vulnerability object
        Args:
            osv_vuln (dict) : the vulnerability returned by the API
            dependency (Dependency) : the dependency to analyse
            severity (str) : the severity of the vulnerability
        Returns:
            A Vulnerability object corresponding to the vulnerability of the API
        """
        aliases = osv_vuln.get("aliases", [])
        cve_id = next(
            (alias for alias in aliases if alias.startswith("CVE-")),
            None,
        )

        classes = {
            "LOW": LowVulnerability,
            "MEDIUM": MediumVulnerability,
            "HIGH": HighVulnerability,
            "CRITICAL": CriticalVulnerability,
        }

        return classes[severity](
            id_vulnerability=None,
            osv_id=osv_vuln["id"],
            cve_id=cve_id,
            package=dependency.name,
            version_package=dependency.version,
        )
