import json

from business_object.dependency import Dependency


class JsonService:
    """Service that handles file.json methods"""

    def parse_dependencies(self, content: bytes) -> list[Dependency]:
        """
        Find all the dependencies from a content (json)
        Args:
            content (bytes): content of a file.json
        Returns:
            List of Dependency object found in the file
        """
        data = json.loads(content)
        list_dep = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        return [Dependency(name=n, version=v) for n, v in list_dep.items()]
