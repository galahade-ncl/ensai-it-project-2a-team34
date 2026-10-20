import re
from urllib.parse import quote

import requests

from business_object.dependency import Dependency

DEPSDEV_URL = "https://api.deps.dev/v3"

# Ecosystem names (OSV) -> system names (deps.dev)
DEPSDEV_SYSTEMS = {
    "PyPI": "PYPI",
    "npm": "NPM",
    "Maven": "MAVEN",
    "crates.io": "CARGO",
}


class API_DEPSDEV:
    """Class that handles calls to the deps.dev API"""

    @staticmethod
    def clean_version(version: str | None) -> str | None:
        """
        Keep only an exact version ('^1.2.0' -> '1.2.0', '>=1.0,<2' -> '1.0')
        Returns None if no version can be extracted
        """
        if not version:
            return None
        m = re.search(r"\d+(\.\d+)*([-+.\w]*)", version)
        return m.group(0) if m else None

    @staticmethod
    def find_licences(dependency: Dependency, ecosystem: str) -> list[str]:
        """
        Find the licences (SPDX identifiers) of a dependency
        Args:
            dependency (Dependency): dependency to look for
            ecosystem (str): OSV ecosystem name (ex: 'PyPI')
        Returns:
            List of licence names, empty if the dependency is unknown to deps.dev
        """
        system = DEPSDEV_SYSTEMS.get(ecosystem)
        if system is None:
            raise ValueError(f"Écosystème non supporté par deps.dev : {ecosystem}")

        name = quote(dependency.name, safe="")  # Maven: 'group:artifact' -> 'group%3Aartifact'
        base = f"{DEPSDEV_URL}/systems/{system}/packages/{name}"

        version = API_DEPSDEV.clean_version(dependency.version)
        if version is None:
            version = API_DEPSDEV._default_version(base)
            if version is None:
                return []

        response = requests.get(f"{base}/versions/{quote(version, safe='')}", timeout=10)
        if response.status_code == 404:  # package or version unknown
            return []
        response.raise_for_status()
        return response.json().get("licenses", [])

    @staticmethod
    def _default_version(base: str) -> str | None:
        """Get the default version of a package when the file gives none"""
        response = requests.get(base, timeout=10)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        for v in response.json().get("versions", []):
            if v.get("isDefault"):
                return v["versionKey"]["version"]
        return None
