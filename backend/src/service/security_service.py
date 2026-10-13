from api_osv.api_osv import API_OSV
from business_object.dependency import Dependency
from business_object.file.dependencyfile import DependencyFile
from business_object.licence import Licence
from business_object.vulnerability.vulnerability import Vulnerability


class SecurityService:
    def parse_dependencies(self, dependencyfile: DependencyFile) -> list[Dependency]:
        """
        Find all the dependencies in the dependencyfile
        Args:
            dependencyfile (DependencyFile): file containing all the dependencies
        Returns:
            List of Dependency object found in the file
        """
        pass

    def detect_ecosystem(self, dependencyfile: DependencyFile) -> str:
        """
        Find the ecosystem related to the type of the dependencyfile
        Args:
            dependencyfile (DependencyFile): file containing all the dependencies
        Returns:
            String object if the name of the ecosystem is found
        """
        filename = DependencyFile.name
        if filename == "requirements.txt":
            return "PyPI"
        if filename == "package.json":
            return "npm"
        if filename == "pom.xml":
            return "Maven"
        raise ValueError(f"Fichier non supporté : {filename}")

    def find_vulnerabilities(
        self, dep_file: DependencyFile
    ) -> list[Vulnerability]:
        """
        Found vulnerabilities from the dependencyfile and with the call of API_OSV
        Args:
            dependencyfile (DependencyFile): file containing all the dependencies
        Returns:
            List of Vulnerability object found related to dependencyfile
        """
        list_vuln = []
        list_dep = SecurityService.parse_dependencies(dependencyfile=dep_file)
        chosen_ecosystem = SecurityService.detect_ecosystem(dependencyfile=dep_file)
        for dep in list_dep:
            list_vuln = list_vuln + API_OSV.find_vulnerabilities(
                dependency=dep, ecosystem=chosen_ecosystem
            )
        return list_vuln

    def find_licences(self, dep_file=DependencyFile) -> list[Licence]:
        """
        Find all the licences in the dependencyfile
        Args:
            dependencyfile (DependencyFile): file containing all the dependencies
        Returns:
            List of Licence object found in the file
        """
        pass
