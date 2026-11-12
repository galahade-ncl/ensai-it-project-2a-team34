import requests
from cvss import CVSS2, CVSS3, CVSS4

from business_object.dependency import Dependency
from business_object.vulnerability.critical_vulnerability import CriticalVulnerability
from business_object.vulnerability.high_vulnerability import HighVulnerability
from business_object.vulnerability.low_vulnerability import LowVulnerability
from business_object.vulnerability.medium_vulnerability import MediumVulnerability
from business_object.vulnerability.vulnerability import Vulnerability
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
        Find all the vulnerabilities linked to a dependency.

        Queries the OSV API for the given dependency and returns
        the vulnerabilities (CVE) that affect it.

        Parameters
        ----------
        dependency : Dependency
            Dependency to analyse through the external API.
        ecosystem : str
            Ecosystem associated with the dependency file (e.g. ``'PyPI'``).

        Returns
        -------
        list of Vulnerability
            Vulnerabilities linked to the dependency. The list is empty
            if none are found.
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
            # call of _get_severity
            severity = API_OSV._get_severity(osv_vuln)

            if severity is None:
                continue

            # call of _to_vulnerability
            vulnerability = API_OSV._to_vulnerability(
                osv_vuln,
                dependency,
                severity,
            )
            vulnerabilities.append(vulnerability)

        return vulnerabilities

    @staticmethod
    @log
    def _get_severity(osv_vuln: dict) -> str | None:
        """
        Determine the severity of a vulnerability from its CVSS vector.

        Reads the CVSS data of an OSV vulnerability entry and converts it
        into a severity level.

        Parameters
        ----------
        osv_vuln : dict
            Vulnerability entry returned by the OSV API.

        Returns
        -------
        str or None
            Severity level of the vulnerability, or None if the
            vulnerability does not represent a risk.
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
    @log
    def _to_vulnerability(osv_vuln: dict, dependency: Dependency, severity: str) -> Vulnerability:
        """
        Transform an OSV API response into a Vulnerability object.

        Builds a Vulnerability from the raw entry returned by the OSV API,
        and links it to the analysed dependency with its severity level.

        Parameters
        ----------
        osv_vuln : dict
            Vulnerability entry returned by the OSV API.
        dependency : Dependency
            Dependency affected by the vulnerability.
        severity : str
            Severity level of the vulnerability.

        Returns
        -------
        Vulnerability
            Vulnerability object corresponding to the API entry.
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
