# import pytest
# from datetime import datetime
from src.service.file_services.toml_service import TomlService

# from src.business_object.dependency import Dependency


def test_toml_string_and_table_versions():
    """ Verify that the version is parsed correctly both as a string (“1.0”) and as a object ({ version = “1.2” })."""
    # GIVEN
    content = b'[dependencies]\nserde = "1.0"\ntokio = { version = "1.2", features = ["full"] }\n'
    list_result = [("serde", "1.0"), ("tokio", "1.2")]

    # WHEN
    list_dep = TomlService().parse_dependencies(content)

    # THEN
    for i in range(len(list_dep)):
        assert list_dep[i].name == list_result[i][0]
        assert list_dep[i].version == list_result[i][1]


def test_toml_dependency_without_version():
    """ Check that a dependency without a version (e.g., path = ...) returns None."""
    # GIVEN
    content = b'[dependencies]\nlocal = { path = "../local" }\n'
    list_result = [("local", None)]

    # WHEN
    list_dep = TomlService().parse_dependencies(content)

    # THEN
    for i in range(len(list_dep)):
        assert list_dep[i].name == list_result[i][0]
        assert list_dep[i].version == list_result[i][1]


def test_toml_no_dependencies_section():
    """ Verify that a TOML file without a [dependencies] section returns an empty list."""
    # GIVEN
    content = b'[package]\nname = "x"\n'
    list_result = []

    # WHEN
    list_dep = TomlService().parse_dependencies(content)

    # THEN
    assert list_dep == list_result
