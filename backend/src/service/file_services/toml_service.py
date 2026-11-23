import re
import tomllib

from business_object.dependency import Dependency

# PEP 508: "name[extra] >=1.0 ; marker" -> name, then the version specifier
PEP508 = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[[^\]]*\])?\s*([^;]*)")
EXACT = re.compile(r"^\s*==\s*([^\s,*;]+)\s*$")


class TomlService:
    """
    Service that parses ``.toml`` dependency files
    (``Cargo.toml`` and ``pyproject.toml``).
    """

    def parse_dependencies(self, content: bytes) -> list[Dependency]:
        """
        Find all the dependencies in the content of a ``.toml`` file.

        A file with a ``[project]`` table is a ``pyproject.toml``,
        anything else is read as a ``Cargo.toml``.

        Parameters
        ----------
        content : bytes
            Content of the ``.toml`` file.

        Returns
        -------
        list of Dependency
            Dependencies found in the file. A dependency of a
            ``pyproject.toml`` has a version only if it is pinned with ``==``.

        Raises
        ------
        ValueError
            If a ``pyproject.toml`` has no ``[project] dependencies`` list.
        """
        data = tomllib.loads(content.decode("utf-8"))
        if "project" in data:
            return self._from_pyproject(data)
        return self._from_cargo(data)

    @staticmethod
    def _from_cargo(data: dict) -> list[Dependency]:
        """Read the ``[dependencies]`` table of a Cargo.toml."""
        list_dep = []
        for name, spec in data.get("dependencies", {}).items():
            version = spec if isinstance(spec, str) else spec.get("version")
            list_dep.append(Dependency(name=name, version=version))
        return list_dep

    @staticmethod
    def _from_pyproject(data: dict) -> list[Dependency]:
        """Read the ``[project] dependencies`` list of a pyproject.toml."""
        specs = data["project"].get("dependencies")
        if specs is None:
            raise ValueError("pyproject.toml: no [project] dependencies list found")
        list_dep = []
        for spec in specs:
            match = PEP508.match(spec)
            if match:
                exact = EXACT.match(match.group(2))
                list_dep.append(
                    Dependency(name=match.group(1), version=exact.group(1) if exact else None)
                )
        return list_dep
