import json
import re
import uuid
from datetime import datetime

from api_deps_dev.api_deps_dev import API_DEPSDEV
from business_object.file.sbomfile import SBOMFile
from business_object.vulnerability.critical_vulnerability import CriticalVulnerability
from business_object.vulnerability.high_vulnerability import HighVulnerability
from business_object.vulnerability.low_vulnerability import LowVulnerability
from business_object.vulnerability.medium_vulnerability import MediumVulnerability
from service.file_services.file_service import FileService

# filename -> purl type
PURL_TYPES = {
    "requirements.txt": "pypi",
    "package.json": "npm",
    "pom.xml": "maven",
    "cargo.toml": "cargo",
}


class SBOMService:
    """Generate the SBOM (CycloneDX, JSON) of a project"""

    @staticmethod
    def _normalize(name: str, ecosystem: str) -> str:
        """PEP 503 normalization for PyPI, lowercase for the others."""
        if ecosystem == "pypi":
            return re.sub(r"[-_.]+", "-", name).lower()
        return name.lower()

    def generate(self, project, vulnerabilities) -> SBOMFile:
        """Generate the SBOM (CycloneDX, JSON) of a project.

        Parameters
        ---------
        project: Project
            Proejct to inventory
        vulnerabilities: list[Vulnerability], optional
            Vulnerabilities found by SecurityService (instance of
            ``CriticalVulnerability``, ``HighVulnerability``,
            ``MediumVulnerability`` or ``LowVulnerability``). They are
            added to the SBOM and linked to the affected . The severity is
            deduced from the class of each vulnerability.

        Returns
        ------
        SbomFile
            SBOM whose content is the JSON document in bytes

        Raises
        ------
        ValueError
            If the project is ''None''.
        """
        if project is None:
            raise ValueError("Cannot generate a SBOM: project is None.")

        file_service = FileService()
        dependencyfile = project.dependencyfile

        # 1) Ecosystem (purl type) from the real filename, e.g. "package.json"
        filename = file_service.get_filename(dependencyfile).lower()
        ecosystem = PURL_TYPES.get(filename, "pypi")

        # 2) Dependencies :
        dependencies = file_service.parse_dependencies(dependencyfile)

        # 3) One CycloneDX component per dependency
        components = []
        seen = set()
        for dependency in dependencies:
            name = self._normalize(dependency.name, ecosystem)
            version = API_DEPSDEV.clean_version(dependency.version)  # '^1.2.0' -> '1.2.0'

            purl = f"pkg:{ecosystem}/{name.replace(':', '/')}"
            if version:
                purl += f"@{version}"
            if purl in seen:
                continue
            seen.add(purl)

            component = {"type": "library", "bom-ref": purl, "name": name, "purl": purl}
            if version:
                component["version"] = version
            components.append(component)

        # 4) CycloneDX document (built ONCE, after the loop)
        project_name = getattr(project, "name_project", None) or "project"
        date = datetime.now()
        document = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.5",
            "serialNumber": f"urn:uuid:{uuid.uuid4()}",
            "version": 1,
            "metadata": {
                "timestamp": date.isoformat(),
                "tools": {"components": [{"type": "application", "name": "CleanOps"}]},
                "component": {
                    "type": "application",
                    "bom-ref": project_name,
                    "name": project_name,
                },
            },
            "components": components,
            "dependencies": [{"ref": project_name, "dependsOn": [c["bom-ref"] for c in components]}]
            + [{"ref": c["bom-ref"], "dependsOn": []} for c in components],
        }

        # 5) Vulnerabilities
        if vulnerabilities:
            document["vulnerabilities"] = []
            for vulnerability in vulnerabilities:
                if isinstance(vulnerability, CriticalVulnerability):
                    severity = "critical"
                elif isinstance(vulnerability, HighVulnerability):
                    severity = "high"
                elif isinstance(vulnerability, MediumVulnerability):
                    severity = "medium"
                elif isinstance(vulnerability, LowVulnerability):
                    severity = "low"
                else:
                    severity = "unknown"

                entry = {
                    "id": vulnerability.osv_id or vulnerability.cve_id,
                    "source": {"name": "OSV", "url": "https://osv.dev"},
                    "ratings": [{"severity": severity}],
                }
                if vulnerability.cve_id and vulnerability.cve_id != entry["id"]:
                    entry["references"] = [{"id": vulnerability.cve_id, "source": {"name": "NVD"}}]
                package = self._normalize(vulnerability.package or "", ecosystem)
                refs = [c["bom-ref"] for c in components if c["name"] == package]
                if refs:
                    entry["affects"] = [{"ref": refs[0]}]
                document["vulnerabilities"].append(entry)

        return SBOMFile(
            name=f"{project_name}_sbom.json",
            content=json.dumps(document, indent=2).encode("utf-8"),
            type_file="json",
            date=date,
        )

    # Temporaire
    def create_empty_sbom(self):
        return SBOMFile(name="Empty", content=b"0", type_file="json", date=None)
