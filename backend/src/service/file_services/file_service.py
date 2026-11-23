from business_object.dependency import Dependency
from business_object.file.dependencyfile import DependencyFile
from service.file_services.json_service import JsonService
from service.file_services.lock_service import LockService
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
    """
    Service that handles business logic related to a file.
    """

    @log
    def get_filename(self, dependencyfile: DependencyFile) -> str:
        """
        Get the full filename of the dependency file.

        Parameters
        ----------
        dependencyfile : DependencyFile
            File containing the dependencies.

        Returns
        -------
        str
            Name of the file with its extension (e.g. ``'requirements.txt'``).
        """
        return f"{dependencyfile.name}.{dependencyfile.type_file.lstrip('.')}"

    @log
    def parse_dependencies(self, dependencyfile: DependencyFile) -> list[Dependency]:
        """
        Find all the dependencies in the dependency file.

        The parser is chosen according to the extension of the file
        (``txt``, ``json``, ``xml`` or ``toml``).

        Parameters
        ----------
        dependencyfile : DependencyFile
            File containing all the dependencies.

        Returns
        -------
        list of Dependency
            Dependencies found in the file.

        Raises
        ------
        ValueError
            If the extension of the file is not supported.
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

        elif extension == "lock":
            return LockService().parse_dependencies(dependencyfile.content)

        raise ValueError(f"Type de fichier non supporté : {extension}")
