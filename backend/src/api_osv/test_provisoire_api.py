# from api_osv import API_OSV
# from business_object.dependency import Dependency

# dep = Dependency(1, "requests", "2.19.0")
# vulns = API_OSV.find_vulnerabilities(dep, "PyPI")

# for v in vulns:
#     print(type(v).__name__, v.osv_id, v.cve_id, v.package, v.version_package)
# python backend/src/api_osv/test_provisoire_api.py
import sys
from pathlib import Path

from api_osv import API_OSV
from business_object.dependency import Dependency
from business_object.vulnerability.medium_vulnerability import MediumVulnerability

# The `backend/` directory must be in the PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

cvss_vector = ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N")
vuln = {"severity": [{"type": "CVSS_V3", "score": cvss_vector}]}
print(API_OSV._get_severity(vuln))


osv_vuln = {"id": "GHSA-1234", "aliases": ["CVE-2024-1234"]}
dep = Dependency(1, "requests", "2.19.0")
print(isinstance(API_OSV._to_vulnerability(osv_vuln, dep, "MEDIUM"), MediumVulnerability))

if __name__ == "__main__":
    print("Start of the API_OSV manual test...")
    try:
        # 1. Creating the dependency to be tested
        dep = Dependency(1, "requests", "2.19.0")
        print(f"Dependency Test : {dep.name}@{dep.version}")

        # 2. OSV API Call
        vulns = API_OSV.find_vulnerabilities(dep, "PyPI")

        # 3. Displaying Results
        if not vulns:
            print("No vulnerabilities found.")
        else:
            print(f"{len(vulns)} vulnerability(ies) found :\n")
            for v in vulns:
                print(
                    f"  - [{v.__class__.__name__}] {v.osv_id} | CVE: {v.cve_id or 'N/A'} | {v.package}@{v.version_package}"
                )

    except Exception as e:
        print(f"Test Failed : {e}")
        import traceback

        traceback.print_exc()
