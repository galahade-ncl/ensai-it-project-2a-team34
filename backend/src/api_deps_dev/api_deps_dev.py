import re
from urllib.parse import quote

import requests

from business_object.dependency import Dependency
from business_object.licence import Licence

DEPSDEV_URL = "https://api.deps.dev/v3"

# Ecosystem names (OSV) -> system names (deps.dev)
DEPSDEV_SYSTEMS = {
    "PyPI": "PYPI",
    "npm": "NPM",
    "Maven": "MAVEN",
    "crates.io": "CARGO",
}

LICENCE_RISK = {
    "MIT": "low",
    "Apache-2.0": "low",
    "BSD-2-Clause": "low",
    "BSD-3-Clause": "low",
    "ISC": "low",
    "MPL-2.0": "medium",
    "LGPL-2.1": "medium",
    "LGPL-3.0": "medium",
    "GPL-2.0": "high",
    "GPL-3.0": "high",
    "AGPL-3.0": "high",
}
DEFAULT_RISK = "unknown"  # Missing, non-standard, or unrecognized license


class API_DEPSDEV:
    """Class that handles calls to the deps.dev API"""

    @staticmethod
    def clean_version(version: str | None) -> str | None:
        """
        Extract an exact version number from a version specifier.

        Strips range operators and constraints (e.g. ``^``, ``>=``, ``<``)
        and keeps only the first version number found.

        Parameters
        ----------
         version : str or None
            Version specifier to clean (e.g. ``'^1.2.0'`` or ``'>=1.0,<2'``).

        Returns
        -------
        str or None
            The extracted exact version (e.g. ``'1.2.0'`` or ``'1.0'``),
            or None if no version can be extracted.

        Examples
        --------
        >>> clean_version('^1.2.0')
        '1.2.0'
        >>> clean_version('>=1.0,<2')
        '1.0'
        """
        if not version:
            return None
        m = re.search(r"\d+(\.\d+)*([-+.\w]*)", version)
        return m.group(0) if m else None

    @staticmethod
    def find_licences(dependency: Dependency, ecosystem: str) -> list[str]:
        """
        Find the licences of a dependency.

        Queries the deps.dev API for the given dependency and returns
        the SPDX identifiers of its licences.

        Parameters
        ----------
        dependency : Dependency
            Dependency to look up.
        ecosystem : str
            OSV ecosystem name (e.g. ``'PyPI'``).

        Returns
        -------
        list of str
            Licence names (SPDX identifiers). The list is empty if the
            dependency is unknown to deps.dev.
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
        return API_DEPSDEV._to_licences(response.json().get("licenses", []))

    @staticmethod
    def _default_version(base: str) -> str | None:
        """
        Get the default version of a package.

        Used as a fallback when the dependency file does not specify
        any version for the package.

        Parameters
        ----------
        base : str
            Base URL used to query the package information.

        Returns
        -------
        str or None
            The default version of the package, or None if it cannot
            be determined.
        """
        response = requests.get(base, timeout=10)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        for v in response.json().get("versions", []):
            if v.get("isDefault"):
                return v["versionKey"]["version"]
        return None

    @staticmethod
    def _to_licences(names: list[str]) -> list[Licence]:
        """
        Convert licence names into Licence objects.

        Maps each SPDX identifier returned by deps.dev to a Licence object
        and assigns it a risk level based on LICENCE_RISK.

        Parameters
        ----------
        names : list of str
            Licence names (SPDX identifiers) returned by deps.dev.

        Returns
        -------
        list of Licence
            Licence objects with their risk level. The risk level is
            ``'unknown'`` if the licence is not in LICENCE_RISK.
        """
        return [
            Licence(name=name, risk_level=LICENCE_RISK.get(name, DEFAULT_RISK)) for name in names
        ]
