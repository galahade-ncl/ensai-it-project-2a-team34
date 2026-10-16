from api_osv.api_osv import API_OSV
from business_object.file.dependencyfile import DependencyFile
from business_object.licence import Licence
from business_object.vulnerability.vulnerability import Vulnerability
from service.file_services.file_service import FileService
from utils.log_utils import log


class SecurityService:
    @log
    def detect_ecosystem(self, dependencyfile: DependencyFile) -> str:
        """
        Find the ecosystem related to the type of the dependencyfile
        Args:
            dependencyfile (DependencyFile): file containing all the dependencies
        Returns:
            String object if the name of the ecosystem is found
        """

        SUPPORTED_FILES = {
            "requirements.txt": "PyPI",
            "package.json": "npm",
            "pom.xml": "Maven",
            "Cargo.toml": "crates.io",
        }

        filename = FileService().get_filename(dependencyfile)

        if filename not in SUPPORTED_FILES:
            raise ValueError(
                f"Fichier non supporté : {filename}. "
                f"Fichiers acceptés : {', '.join(SUPPORTED_FILES)}"
            )
        return SUPPORTED_FILES[filename]

    @log
    def find_vulnerabilities(self, dep_file: DependencyFile) -> list[Vulnerability]:
        """
        Found vulnerabilities from the dependencyfile and with the call of API_OSV
        Args:
            dependencyfile (DependencyFile): file containing all the dependencies
        Returns:
            List of Vulnerability object found related to dependencyfile
        """
        list_vuln = []
        list_dep = FileService.parse_dependencies(dependencyfile=dep_file)
        chosen_ecosystem = SecurityService.detect_ecosystem(dependencyfile=dep_file)
        for dep in list_dep:
            list_vuln = list_vuln + API_OSV.find_vulnerabilities(
                dependency=dep, ecosystem=chosen_ecosystem
            )
        return list_vuln

    @log
    def find_licences(self, dep_file=DependencyFile) -> list[Licence]:
        """
        Find all the licences in the dependencyfile
        Args:
            dependencyfile (DependencyFile): file containing all the dependencies
        Returns:
            List of Licence object found in the file
        """
        pass
