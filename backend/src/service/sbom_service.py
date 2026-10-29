import json
import re
import uuid
from datetime import datetime, timezone

from business_object.file.sbomfile import SbomFile
from business_object.project import Project

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
            Vulnerabilities found by SecurityService. They are
            qdded to the SBOM and linked to the affected package
        
        Returns
        ------
        SbomFile
            SBOM whose content is the JSON document in bytes
        
        Raises
        ------

        ValueError
            If the project is ''None''
        """

        
