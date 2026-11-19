import tomllib

from business_object.dependency import Dependency


class TomlService:
    """
    Service that parses ``.toml`` dependency files (``Cargo.toml``).
    """

    def parse_dependencies(self, content: bytes) -> list[Dependency]:
        """
        Find all the dependencies in the content of a ``.toml`` file.

        Reads the ``[dependencies]`` table.

        Parameters
        ----------
        content : bytes
            Content of the ``.toml`` file.

        Returns
        -------
        list of Dependency
            Dependencies found in the file.
        """
        data = tomllib.loads(content.decode("utf-8"))
        list_dep = []
        for name, spec in data.get("dependencies", {}).items():
            version = spec if isinstance(spec, str) else spec.get("version")
            list_dep.append(Dependency(name=name, version=version))
        return list_dep
