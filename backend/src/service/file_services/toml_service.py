import tomllib

from business_object.dependency import Dependency


class TomlService:
    """Service that handles file.toml methods"""

    def parse_dependencies(self, content: bytes) -> list[Dependency]:
        """
        Find all the dependencies from a content (toml)
        Args:
            content (bytes): content of a file.toml
        Returns:
            List of Dependency object found in the file
        """
        data = tomllib.loads(content.decode("utf-8"))
        list_dep = []
        for name, spec in data.get("dependencies", {}).items():
            version = spec if isinstance(spec, str) else spec.get("version")
            list_dep.append(Dependency(name=name, version=version))
        return list_dep
