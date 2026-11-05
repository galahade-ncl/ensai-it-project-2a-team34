import json
from types import SimpleNamespace

import pytest

from business_object.file.dependencyfile import DependencyFile
from business_object.file.sbomfile import SBOMFile
from business_object.project import Project
from business_object.vulnerability.critical_vulnerability import CriticalVulnerability
from business_object.vulnerability.high_vulnerability import HighVulnerability
from business_object.vulnerability.low_vulnerability import LowVulnerability
from business_object.vulnerability.medium_vulnerability import MediumVulnerability
from service.sbom_service import SBOMService

# A tester SBOMService.generate() et SBOMfile.get_duty()

#helpers
def make_dependency(name, version=None):  
    """Fake Dependency: generate() only reads .name and .version
        expects Dependency objects
    """
    return SimpleNamespace(name=name, version=version)

# fixture
@pytest.fixture
def user():
    """fictive user because project needs a user"""
    return SimpleNamespace(
        id_user=1, username="Jean-Michel", email="jean-michel@mail.fr", password="0000"
    )

@pytest.fixture
def make_project(user): 
    """Factory building a real project whose dependency file has the given name"""

    def _make_project(filename="requirements.txt", name_project="demo"):
        return Project(
            name_project=name_project,
            user=user,
            secretHMACkey=bytes.fromhex(
                "7f2cd2cada12a1c7f6550f4b9aa3873776d6b0228b2d9c1596dcdf8eda301930"
            ),
            id_project=1,
            dependencyfile=DependencyFile(name=filename, content=b"", type_file="dependency"),
        )

    return _make_project


@pytest.fixture
def project(make_project):
    """Fictive Python project (requirements.txt)"""
    return make_project("requirements.txt")

@pytest.fixture
def file_service(monkeypatch):
    """Replace FileService inside sbom_service.

    get_filename returns the name of the file; parse_dependencies returns
    `fake.parsed` and records each call in `fake.calls`.
    """
    fake = SimpleNamespace(
        parsed=[
            make_dependency("requests", "2.31.0"),
            make_dependency("Django_REST.framework", "3.15.1"),
            make_dependency("pandas", ">=2.0"),
            make_dependency("flask", None),
        ],
        calls=[],
    )

    class FakeFileService:
        def get_filename(self, file):
            return file.name

        def parse_dependencies(self, file):
            fake.calls.append(file)
            return fake.parsed

    monkeypatch.setattr("service.sbom_service.FileService", FakeFileService)
    return fake


@pytest.fixture(autouse=True)
def clean_version(monkeypatch):
    """Replace API_DEPSDEV.clean_version: removes '^', '~', '=' and 'v'
    prefixes and returns None for a range (e.g. '>=2.0') or no version."""

    def fake_clean_version(version):
        if not version or version[0] in "<>!":
            return None
        return version.lstrip("^~=v")

    monkeypatch.setattr(
        "service.sbom_service.API_DEPSDEV", SimpleNamespace(clean_version=fake_clean_version)
    )


#SBOMFile.get_duty()
def test_sbomfile_get_duty():
    sbom=SBOMFile(name="demo_sbom.json",content=b"{}",type_file="json",date=None)
    assert sbom.get_duty()=="sbom"


# SBOMService.generate()
def test_generate_successful(project,file_service):
    sbom = SBOMService().generate(project)
    document = json.loads(sbom.content)
    assert isinstance(sbom, SBOMFile)
    assert sbom.name == "demo_sbom.json" and sbom.type_file == "json"
    assert document["bomFormat"] == "CycloneDX"
    assert [c["name"] for c in document["components"]] == [
        "requests",
        "django-rest-framework",
        "pandas",
        "flask",
    ]
    assert "version" not in document["components"][2]
    assert document["dependencies"][0]["dependsOn"][0] == "pkg:pypi/requests@2.31.0"


def test_generate_failed():
    with pytest.raises(ValueError):
        SBOMService().generate(None)

def test_generate_parses_dependency_file_when_no_dependencies(project, file_service):
    SBOMService().generate(project)
    assert file_service.calls == [project.dependencyfile]

def test_generate_with_given_dependencies(project,file_service):
    dependencies = [make_dependency("numpy", "1.26.4"), make_dependency("numpy", "1.26.4")]
    sbom = SBOMService().generate(project, dependencies=dependencies)

    assert len(json.loads(sbom.content)["components"]) == 1  # duplicate removed
    assert file_service.calls == []  # the file is not parsed again

def test_generate_uses_clean_version(project, file_service):
    sbom = SBOMService().generate(project, dependencies=[make_dependency("numpy", "^1.26.4")])
    component = json.loads(sbom.content)["components"][0]
    assert component["version"] == "1.26.4"
    assert component["purl"] == "pkg:pypi/numpy@1.26.4"

def test_generate_without_dependencies(project, file_service):
    file_service.parsed = []
    document = json.loads(SBOMService().generate(project).content)
    assert document["components"] == []
    assert document["dependencies"] == [{"ref": "demo", "dependsOn": []}]

#test of generate for every kind of depency file(txt, toml, json,xml)
@pytest.mark.parametrize(
    "filename, dependencies, expected_purls",
    [
        # TXT -> pypi
        (
            "requirements.txt",
            [make_dependency("requests", "2.31.0")],
            ["pkg:pypi/requests@2.31.0"],
        ),
        # TOML (Python) -> pypi
        (
            "pyproject.toml",
            [make_dependency("Django_REST.framework", "3.15.1"), make_dependency("flask")],
            ["pkg:pypi/django-rest-framework@3.15.1", "pkg:pypi/flask"],
        ),
        # TOML (Rust) -> cargo, file name is case-insensitive
        (
            "Cargo.toml",
            [make_dependency("serde", "1.0.200")],
            ["pkg:cargo/serde@1.0.200"],
        ),
        # JSON -> npm
        (
            "package.json",
            [make_dependency("react", "^18.3.1"), make_dependency("@types/node", "20.1.0")],
            ["pkg:npm/react@18.3.1", "pkg:npm/@types/node@20.1.0"],
        ),
        # XML -> maven, "group:artifact" becomes "group/artifact"
        (
            "pom.xml",
            [make_dependency("org.junit:junit", "4.13")],
            ["pkg:maven/org.junit/junit@4.13"],
        ),
    ],
)
def test_generate_by_dependency_file_type(
    make_project, file_service, filename, dependencies, expected_purls
):
    project = make_project(filename)
    sbom = SBOMService().generate(project, dependencies=dependencies)
    purls = [c["purl"] for c in json.loads(sbom.content)["components"]]
    assert purls == expected_purls


def test_generate_unknown_file_defaults_to_pypi(make_project, file_service):
    project = make_project("deps.cfg")
    sbom = SBOMService().generate(project, dependencies=[make_dependency("numpy", "1.26.4")])
    assert json.loads(sbom.content)["components"][0]["purl"] == "pkg:pypi/numpy@1.26.4"

#test of generate with vulnerabilities
def test_generate_with_vulnerabilities(project,file_service):
    vulnerabilities = [
        MediumVulnerability(1, "GHSA-9wx4-h78v-vm56", "CVE-2024-35195", "requests", "2.31.0"),
        CriticalVulnerability(2, "PYSEC-2024-1", None, "Flask", ""),
    ]
    document = json.loads(SBOMService().generate(project, vulnerabilities=vulnerabilities).content)
    medium, critical = document["vulnerabilities"]

    assert medium["id"] == "GHSA-9wx4-h78v-vm56"
    assert medium["ratings"] == [{"severity": "medium"}]
    assert medium["affects"] == [{"ref": "pkg:pypi/requests@2.31.0"}]
    assert medium["references"][0]["id"] == "CVE-2024-35195"

    assert critical["ratings"] == [{"severity": "critical"}]
    assert critical["affects"] == [{"ref": "pkg:pypi/flask"}]
    assert "references" not in critical

def test_generate_vulnerability_on_unlisted_package(project, file_service):
    vulnerability = HighVulnerability(1, "OSV-1", None, "numpy", "1.0")
    document = json.loads(SBOMService().generate(project, vulnerabilities=[vulnerability]).content)
    assert "affects" not in document["vulnerabilities"][0]

"""  this following decorator offer the possibility to do a test for every
subclass without creating a function for each of them
"""
@pytest.mark.parametrize(
    "vulnerability_class, expected",
    [
        (CriticalVulnerability, "critical"),
        (HighVulnerability, "high"),
        (MediumVulnerability, "medium"),
        (LowVulnerability, "low"),
    ],
)
def test_generate_severity_from_subclass(project,file_service,vulnerability_class, expected):
    vulnerability = vulnerability_class(1, "OSV-1", None, "requests", "2.31.0")
    document = json.loads(SBOMService().generate(project, vulnerabilities=[vulnerability]).content)
    assert document["vulnerabilities"][0]["ratings"] == [{"severity": expected}]
