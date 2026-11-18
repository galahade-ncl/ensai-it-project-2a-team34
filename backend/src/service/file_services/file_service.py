from business_object.dependency import Dependency
from business_object.file.dependencyfile import DependencyFile
from service.file_services.json_service import JsonService
from service.file_services.toml_service import TomlService
from service.file_services.txt_service import TxtService
from service.file_services.xml_service import XmlService

# from java_service import JavaService
# from js_service import JsService
# from py_service import PyService
# from business_object.project import Project
# from business_object.user import User
from utils.log_utils import log


class FileService:
    """Service that handles business logic related to a file"""

    @log
    def get_filename(self, dependencyfile: DependencyFile) -> str:
        """
        Get the filename of the dependency file
        Args:
            dependencyfile (DependencyFile): file containing dependencies
        Return:
            String object containing the name of the file with the type of the file (ex: 'requirements.txt')
        """
        return f"{dependencyfile.name}.{dependencyfile.type_file.lstrip('.')}"

    @log
    def parse_dependencies(self, dependencyfile: DependencyFile) -> list[Dependency]:
        """
        Find all the dependencies in the dependencyfile
        Args:
            dependencyfile (DependencyFile): file containing all the dependencies
        Returns:
            List of Dependency object found in the file
        """
        extension = dependencyfile.type_file.lstrip(".").lower()

        if extension == "txt":
            return TxtService().parse_dependencies(dependencyfile.content)

        elif extension == "json":
            return JsonService().parse_dependencies(dependencyfile.content)

        elif extension == "xml":
            return XmlService().parse_dependencies(dependencyfile.content)

        elif extension == "toml":
            return TomlService().parse_dependencies(dependencyfile.content)

        raise ValueError(f"Type de fichier non supporté : {extension}")
