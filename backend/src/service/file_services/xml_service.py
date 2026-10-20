import xml.etree.ElementTree as ET

from business_object.dependency import Dependency


class XmlService:
    """Service that handles file.xml methods"""

    def parse_dependencies(self, content: bytes) -> list[Dependency]:
        """
        Find all the dependencies from a content (xml)
        Args:
            content (bytes): content of a file.xml
        Returns:
            List of Dependency object found in the file
        """
        root = ET.fromstring(content)
        list_dep = []
        for d in root.iterfind(".//{*}dependencies/{*}dependency"):
            group = d.findtext("{*}groupId")
            artifact = d.findtext("{*}artifactId")
            version = d.findtext("{*}version")
            list_dep.append(Dependency(name=f"{group}:{artifact}", version=version))
        return list_dep
