from api_deps_dev.api_deps_dev import API_DEPSDEV
from api_osv.api_osv import API_OSV
from business_object.file.dependencyfile import DependencyFile
from business_object.licence import Licence
from business_object.vulnerability.vulnerability import Vulnerability
from service.file_services.file_service import FileService
from utils.log_utils import log


class SecurityService:
    """
    Service that finds the vulnerabilities and the licences of the
    dependencies of a project.
    """

    @log
    def detect_ecosystem(self, dependencyfile: DependencyFile) -> str:
        """
        Find the ecosystem related to the dependency file.

        Parameters
        ----------
        dependencyfile : DependencyFile
            File containing all the dependencies.

        Returns
        -------
        str
            Name of the ecosystem (``'PyPI'``, ``'npm'``, ``'Maven'`` or
            ``'crates.io'``).

        Raises
        ------
        ValueError
            If the file is not supported.
        """

        SUPPORTED_FILES = {
            "requirements.txt": "PyPI",
            "pipfile.lock": "PyPI",
            "poetry.lock": "PyPI",
            "pyproject.toml": "PyPI",
            "package.json": "npm",
            "pom.xml": "Maven",
            "cargo.toml": "crates.io",
        }

        filename = FileService().get_filename(dependencyfile).lower()

        if filename not in SUPPORTED_FILES:
            raise ValueError(
                f"Fichier non supporté : {filename}. "
                f"Fichiers acceptés : {', '.join(SUPPORTED_FILES)}"
            )
        return SUPPORTED_FILES[filename]

    @log
    def find_vulnerabilities(self, dep_file: DependencyFile) -> list[Vulnerability]:
        """
        Find the vulnerabilities of the dependencies using the OSV API.

        Parameters
        ----------
        dep_file : DependencyFile
            File containing all the dependencies.

        Returns
        -------
        list of Vulnerability
            Vulnerabilities found for the dependencies of the file.
        """
        list_vuln = []
        chosen_ecosystem = SecurityService().detect_ecosystem(dependencyfile=dep_file)
        list_dep = FileService().parse_dependencies(dependencyfile=dep_file)
        for dep in list_dep:
            list_vuln = list_vuln + API_OSV.find_vulnerabilities(
                dependency=dep, ecosystem=chosen_ecosystem
            )
        return list_vuln

    @log
    def find_licences(self, dep_file: DependencyFile) -> list[Licence]:
        """
        Find all the licences of the dependencies using the deps.dev API.

        Parameters
        ----------
        dep_file : DependencyFile
            File containing all the dependencies.

        Returns
        -------
        list of Licence
            Licences found in the file, without duplicates.
        """
        ecosystem = self.detect_ecosystem(dependencyfile=dep_file)
        list_dep = FileService().parse_dependencies(dependencyfile=dep_file)

        list_licence = []
        for dep in list_dep:
            for licence in API_DEPSDEV.find_licences(dependency=dep, ecosystem=ecosystem):
                if licence not in list_licence:
                    list_licence.append(licence)
        return list_licence
