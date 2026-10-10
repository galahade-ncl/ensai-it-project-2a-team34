from business_object.file.dependencyfile import DependencyFile


class SecurityService:
    def detect_ecosystem(dependencyfile: DependencyFile) -> str:
        """Return if exist the name of the exosystemm related to the file"""
        filename = DependencyFile.name
        if filename == "requirements.txt":
            return "PyPI"
        if filename == "package.json":
            return "npm"
        if filename == "pom.xml":
            return "Maven"
        raise ValueError(f"Fichier non supporté : {filename}")
