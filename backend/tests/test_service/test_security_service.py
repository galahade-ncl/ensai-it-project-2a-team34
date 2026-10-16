import pytest
from src.business_object.file.dependencyfile import DependencyFile
from src.service.security_service import SecurityService


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
    # GIVEN
    dependencyfile = DependencyFile(name=name, type_file=type_file, content=b"")

    # WHEN
    ecosystem_found = SecurityService().detect_ecosystem(dependencyfile)

    # THEN
    assert ecosystem_found == expected


def test_detect_ecosystem_failed():
    # GIVEN
    dependencyfile = DependencyFile(name="composer", type_file="json", content=b"")

    # THEN
    with pytest.raises(ValueError):
        SecurityService().detect_ecosystem(dependencyfile)
