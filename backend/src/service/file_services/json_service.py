import json

from business_object.dependency import Dependency


class JsonService:
    """
    Service that parses ``.json`` dependency files (``package.json``).
    """

    def parse_dependencies(self, content: bytes) -> list[Dependency]:
        """
        Find all the dependencies in the content of a ``.json`` file.

        Reads both ``dependencies`` and ``devDependencies``.

        Parameters
        ----------
        content : bytes
            Content of the ``.json`` file.

        Returns
        -------
        list of Dependency
            Dependencies found in the file.
        """
        data = json.loads(content)
        list_dep = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        return [Dependency(name=n, version=v) for n, v in list_dep.items()]
