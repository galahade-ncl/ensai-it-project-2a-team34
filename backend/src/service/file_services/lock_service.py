import json
import tomllib

from business_object.dependency import Dependency


class LockService:
    """
    Service that parses ``.lock`` dependency files (``Pipfile.lock`` and ``poetry.lock``).
    """

    def parse_dependencies(self, content: bytes) -> list[Dependency]:
        """
        Find all the dependencies in the content of a ``.lock`` file.

        ``Pipfile.lock`` is JSON and ``poetry.lock`` is TOML, so the format is
        recognized from the content. Lock files give exact versions.

        Parameters
        ----------
        content : bytes
            Content of the ``.lock`` file.

        Returns
        -------
        list of Dependency
            Dependencies found in the file.

        Raises
        ------
        ValueError
            If the content is neither valid JSON nor valid TOML.
        """
        text = content.decode("utf-8-sig")
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return self._from_poetry(tomllib.loads(text))
        return self._from_pipfile(data)

    @staticmethod
    def _from_pipfile(data: dict) -> list[Dependency]:
        """Read the ``default`` and ``develop`` sections of a Pipfile.lock."""
        list_dep = []
        for section in ("default", "develop"):
            for name, info in data.get(section, {}).items():
                version = info.get("version", "")
                list_dep.append(
                    Dependency(name=name, version=version[2:] if version.startswith("==") else None)
                )
        return list_dep

    @staticmethod
    def _from_poetry(data: dict) -> list[Dependency]:
        """Read the ``[[package]]`` tables of a poetry.lock."""
        return [
            Dependency(name=p["name"], version=p.get("version")) for p in data.get("package", [])
        ]
