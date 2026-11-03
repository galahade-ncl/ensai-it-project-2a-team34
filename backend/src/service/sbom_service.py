import json
import re
import uuid
from datetime import datetime, timezone

from business_object.file.sbomfile import SbomFile
from business_object.vulnerability.critical_vulnerability import CriticalVulnerability
from business_object.vulnerability.high_vulnerability import HighVulnerability
from business_object.vulnerability.medium_vulnerability_vulnerability import MediumVulnerability
from business_object.vulnerability.low_vulnerability import LowVulnerability
class SBOMService:
    """Generate the SBOM of a project

    The SBOM lists every component of the audited project and 
    the dependencies between them. It is exported in the JSON format
    """

    def generate(self, project, dependencies=None, vulnerabilities=None) -> SbomFile:
        """Generate the SBOM of a project.

        Parameters
        ---------
        project: Project
            Proejct to inventory
        dependencies: list[str], optional
            Dependencies of the project
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
            raise ValueError("Cannot generate a SBOM:project is None.")
        
        # 1)Ecosystem (purl type) deduced from the dependency file name
        dependencyfile=getattr(project, "dependencyfile",None)
        filename=(getattr(dependencyfile, "name","")or"").split("/")[-1].lower()
        ecosystems={"package.json":"npm","pom.xml": "maven"}
        ecosystem=ecosystems.get(filename,"pypi")

        # 2) Dependencies: 
        if dependencies is None: 
            content=getattr(dependencyfile,"content",None) or b"" #b pour bytes
            if isinstance(content,bytes):
                content=content.decode("utf-8-sig")
            dependencies=content.splitlines()
        
        # 3) CycloneDX xcomponent per dependency
        components=[]
        for dependency in dependencies:
            #cleaning
            line=dependency.split("#")[0].split(";")[0].strip()
            if not line or line.startswith("-"): #empty line, comment or option pip
                continue
            #Extraction
            match=re.match(
                r"^(@?[A-Za-z0-9][A-Za-z0-9._:\-/]*)(\[.*\])?\s*(==|@)?\s*([^\s,<>=!~]*)",
                line,
            )
            #name extraction 
            name=match.group(1)
            #version extraction: only exact version is kept
            version=match.group(4) if match.group(3) else None
            if ecosystem=="pypi":
                name=re.sub(r"[-_.]+", "-", name).lower()  # PEP 503 normalization
            #purl
            purl=f"pkg:{ecosystem}/{name.replace(':','/')}" #package URL
            if version:
                purl+=f"@{version}"
            if purl in [c["bom-ref"] for c in components]:
                continue

            component={"type": "library","bom-ref": purl, "name": name, "purl": purl}
            if version:
                component["version"]=version
            components.apppend(component)

            # 4) CycloneDX document: Dictionary
            project_name=getattr(project,"name_project", None) or "project"
            date=datetime.now(timezone.utc)
            document={
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
                "dependencies":[
                    {"ref": project_name, "dependsOn": [c["bom-ref"] for c in components]}
                ]
                + [{"ref": c["bom-ref"], "dependsOn": []} for c in components],
            }

            # 5) Vulnerabilities
            if vulnerabilities:
                document["vulnerabilities"]=[]
                for vulnerability in vulnerabilities:
                    #severity
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
                        entry["references"] = [
                        {"id": vulnerability.cve_id, "source": {"name": "NVD"}}
                        ]
                    #name of the vulnerable package
                    package=re.sub(r"[-_.]+", "-", vulnerability.package or "").lower()
                    refs = [c["bom-ref"] for c in components if c["name"].lower() == package]
                    if refs:
                        entry["affects"] = [{"ref": refs[0]}]
                    document["vulnerabilities"].append(entry)
        return SbomFile(
            name=f"{project_name}_sbom.json",
            content=json.dumps(document, indent=2).encode("utf-8"),
            type_file="json",
            date=date,
        )

