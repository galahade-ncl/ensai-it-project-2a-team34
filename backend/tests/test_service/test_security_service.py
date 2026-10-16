from unittest.mock import MagicMock, patch

import pytest

from api_osv.api_osv import API_OSV
from business_object.file.dependencyfile import DependencyFile
from service.file_services.file_service import FileService
from service.security_service import SecurityService


@pytest.mark.parametrize(
    "name,type_file,expected",
    [
        ("requirements", "txt", "PyPI"),
        ("package", "json", "npm"),
        ("pom", "xml", "Maven"),
        ("Cargo", "toml", "crates.io"),
    ],
)
def test_detect_ecosystem_successful(name, type_file, expected):
    """ Verify that each supported file (requirements.txt, package.json, pom.xml, Cargo.toml) returns the correct OSV ecosystem."""
    # GIVEN
    dependencyfile = DependencyFile(name=name, type_file=type_file, content=b"")

    # WHEN
    ecosystem_found = SecurityService().detect_ecosystem(dependencyfile)

    # THEN
    assert ecosystem_found == expected


def test_detect_ecosystem_failed():
    """ Verify that a file with an unsupported name (e.g., composer.json) raises a ValueError."""
    # GIVEN
    dependencyfile = DependencyFile(name="composer", type_file="json", content=b"")

    # THEN
    with pytest.raises(ValueError):
        SecurityService().detect_ecosystem(dependencyfile)


def test_find_vulnerabilities_aggregates_results_of_all_dependencies():
    """ Verify that, for a file containing multiple dependencies, the vulnerabilities found by the API for each one are combined into a single list."""
    # GIVEN
    dep1, dep2 = MagicMock(), MagicMock()
    vuln1, vuln2, vuln3 = MagicMock(), MagicMock(), MagicMock()

    # WHEN
    with (
        patch.object(FileService, "parse_dependencies", return_value=[dep1, dep2]),
        patch.object(SecurityService, "detect_ecosystem", return_value="PyPI"),
        patch.object(API_OSV, "find_vulnerabilities", side_effect=[[vuln1, vuln2], [vuln3]]),
    ):
        result = SecurityService().find_vulnerabilities(MagicMock())

    # THEN
    assert result == [vuln1, vuln2, vuln3]


def test_find_vulnerabilities_calls_api_for_each_dependency_with_ecosystem():
    """Verifies that the OSV API is called exactly once per dependency, with the relevant dependency and the detected ecosystem."""
    # GIVEN
    dep1, dep2 = MagicMock(), MagicMock()

    # WHEN
    with (
        patch.object(FileService, "parse_dependencies", return_value=[dep1, dep2]),
        patch.object(SecurityService, "detect_ecosystem", return_value="npm"),
        patch.object(API_OSV, "find_vulnerabilities", return_value=[]) as api,
    ):
        SecurityService().find_vulnerabilities(MagicMock())

    # THEN
    api.assert_any_call(dependency=dep1, ecosystem="npm")
    api.assert_any_call(dependency=dep2, ecosystem="npm")
    assert api.call_count == 2


def test_find_vulnerabilities_no_dependencies_returns_empty_list():
    """Return an empty list and never call the API when the file contains no dependency."""
    # GIVEN
    list_result = []

    # WHEN
    with (
        patch.object(FileService, "parse_dependencies", return_value=list_result),
        patch.object(SecurityService, "detect_ecosystem", return_value="PyPI"),
        patch.object(API_OSV, "find_vulnerabilities") as api,
    ):
        result = SecurityService().find_vulnerabilities(MagicMock())

    # THEN
    assert result == list_result
    api.assert_not_called()


def test_unsupported_file_raises_and_skips_api():
    """ Verify that, if the file is not supported, the error is raised before any parsing or API calls are made."""
    with (
        patch.object(SecurityService, "detect_ecosystem", side_effect=ValueError),
        patch.object(FileService, "parse_dependencies") as parse,
        patch.object(API_OSV, "find_vulnerabilities") as api,
    ):
        with pytest.raises(ValueError):
            SecurityService().find_vulnerabilities(MagicMock())

    parse.assert_not_called()
    api.assert_not_called()


def test_api_error_propagates():
    """ Verify that, if the OSV API fails, the error is not suppressed and is passed back to the caller."""
    with (
        patch.object(FileService, "parse_dependencies", return_value=[MagicMock()]),
        patch.object(SecurityService, "detect_ecosystem", return_value="PyPI"),
        patch.object(API_OSV, "find_vulnerabilities", side_effect=RuntimeError),
    ):
        with pytest.raises(RuntimeError):
            SecurityService().find_vulnerabilities(MagicMock())
