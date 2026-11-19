import xml.etree.ElementTree as ET

from business_object.dependency import Dependency


class XmlService:
    """
    Service that parses ``.xml`` dependency files (``pom.xml``).
    """

    def parse_dependencies(self, content: bytes) -> list[Dependency]:
        """
        Find all the dependencies in the content of a ``.xml`` file.

        Each dependency is named ``'groupId:artifactId'``.

        Parameters
        ----------
        content : bytes
            Content of the ``.xml`` file.

        Returns
        -------
        list of Dependency
            Dependencies found in the file.
        """
        root = ET.fromstring(content)
        list_dep = []
        for d in root.iterfind(".//{*}dependencies/{*}dependency"):
            group = d.findtext("{*}groupId")
            artifact = d.findtext("{*}artifactId")
            version = d.findtext("{*}version")
            list_dep.append(Dependency(name=f"{group}:{artifact}", version=version))
        return list_dep
