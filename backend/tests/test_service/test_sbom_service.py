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

# Tests for SBOMService.generate(), SBOMService.create_empty_sbom()
# and SBOMFile.get_duty().
#
# Current contract: generate(project, vulnerabilities)
#   - dependencies are ALWAYS read back from the project dependency file,
#     the caller can no longer inject them;
#   - vulnerabilities is mandatory: pass [] when there is none.
# Tests that used to inject dependencies therefore go through
# file_service.parsed, which defines what the file is supposed to contain.


# --------------------------------------------------------------- HELPERS
def make_dependency(name, version=None):
    """Fake Dependency: generate() only reads .name and .version."""
    return SimpleNamespace(name=name, version=version)


# -------------------------------------------------------------- FIXTURES
@pytest.fixture
def make_project():
    """
    Factory building a Project whose dependency file has the given name.

    The full filename ("requirements.txt") is split the way the application
    does it: DependencyFile stores the stem on one side and the extension on
    the other.
    """

    def _make_project(filename="requirements.txt", name_project="demo"):
        stem, _, extension = filename.rpartition(".")
        return Project(
            name_project=name_project,
            secretHMACkey=bytes.fromhex(
                "7f2cd2cada12a1c7f6550f4b9aa3873776d6b0228b2d9c1596dcdf8eda301930"
            ),
            id_project=1,
            dependencyfile=DependencyFile(name=stem, content=b"", type_file=extension),
        )

    return _make_project


@pytest.fixture
def project(make_project):
    """Fictive Python project (requirements.txt)."""
    return make_project("requirements.txt")


@pytest.fixture
def file_service(monkeypatch):
    """
    Replace FileService inside sbom_service.

    get_filename applies the same rule as the real service (stem + extension).
    parse_dependencies returns `fake.parsed`: each test may redefine that list
    to choose what the dependency file is supposed to contain. Every file
    actually parsed is recorded in `fake.calls`.
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
            return f"{file.name}.{file.type_file.lstrip('.')}"

        def parse_dependencies(self, file):
            fake.calls.append(file)
            return fake.parsed

    monkeypatch.setattr("service.sbom_service.FileService", FakeFileService)
    return fake


@pytest.fixture(autouse=True)
def clean_version(monkeypatch):
    """Replace API_DEPSDEV.clean_version.

    Strips the '^', '~', '=' and 'v' prefixes, and returns None for a range
    (e.g. '>=2.0') or when no version is given.
    """

    def fake_clean_version(version):
        if not version or version[0] in "<>!":
            return None
        return version.lstrip("^~=v")

    monkeypatch.setattr(
        "service.sbom_service.API_DEPSDEV", SimpleNamespace(clean_version=fake_clean_version)
    )


# -------------------------------- SBOMFile.get_duty()
def test_sbomfile_get_duty():
    sbom = SBOMFile(name="demo_sbom.json", content=b"{}", type_file="json", date=None)
    assert sbom.get_duty() == "sbom"


# -------------------------- SBOMService.generate(): basics
def test_generate_successful(project, file_service):
    sbom = SBOMService().generate(project, [])
    document = json.loads(sbom.content)

    assert isinstance(sbom, SBOMFile)
    assert sbom.name == "demo_sbom.json" and sbom.type_file == "json"
    assert document["bomFormat"] == "CycloneDX"
    assert document["specVersion"] == "1.5"
    assert [c["name"] for c in document["components"]] == [
        "requests",
        "django-rest-framework",
        "pandas",
        "flask",
    ]
    # '>=2.0' is not an exact version: the component carries none
    assert "version" not in document["components"][2]
    assert document["dependencies"][0]["dependsOn"][0] == "pkg:pypi/requests@2.31.0"
    # without any vulnerability, the key is not added to the document
    assert "vulnerabilities" not in document


def test_generate_metadata(project, file_service):
    document = json.loads(SBOMService().generate(project, []).content)

    assert document["serialNumber"].startswith("urn:uuid:")
    assert document["metadata"]["tools"]["components"][0]["name"] == "CleanOps"
    assert document["metadata"]["component"]["name"] == "demo"


def test_generate_failed():
    with pytest.raises(ValueError):
        SBOMService().generate(None, [])


def test_generate_requires_vulnerabilities_argument(project, file_service):
    """vulnerabilities has no default value any more: omitting it must fail."""
    with pytest.raises(TypeError):
        SBOMService().generate(project)


def test_generate_always_parses_the_dependency_file(project, file_service):
    """Dependencies can no longer be injected: the file is always read back."""
    SBOMService().generate(project, [])
    assert file_service.calls == [project.dependencyfile]


def test_generate_removes_duplicates(project, file_service):
    file_service.parsed = [
        make_dependency("numpy", "1.26.4"),
        make_dependency("numpy", "1.26.4"),
    ]
    sbom = SBOMService().generate(project, [])
    assert len(json.loads(sbom.content)["components"]) == 1


def test_generate_uses_clean_version(project, file_service):
    file_service.parsed = [make_dependency("numpy", "^1.26.4")]
    component = json.loads(SBOMService().generate(project, []).content)["components"][0]
    assert component["version"] == "1.26.4"
    assert component["purl"] == "pkg:pypi/numpy@1.26.4"


def test_generate_without_dependencies(project, file_service):
    file_service.parsed = []
    document = json.loads(SBOMService().generate(project, []).content)
    assert document["components"] == []
    assert document["dependencies"] == [{"ref": "demo", "dependsOn": []}]


# --------------------------- generate() for every kind of dependency file
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
        # TOML (Rust) -> cargo, the filename is case-insensitive
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
    file_service.parsed = dependencies
    project = make_project(filename)
    sbom = SBOMService().generate(project, [])
    purls = [c["purl"] for c in json.loads(sbom.content)["components"]]
    assert purls == expected_purls


def test_generate_unknown_file_defaults_to_pypi(make_project, file_service):
    file_service.parsed = [make_dependency("numpy", "1.26.4")]
    project = make_project("deps.cfg")
    sbom = SBOMService().generate(project, [])
    assert json.loads(sbom.content)["components"][0]["purl"] == "pkg:pypi/numpy@1.26.4"


# ----------------------- generate() with vulnerabilities
def test_generate_with_vulnerabilities(project, file_service):
    vulnerabilities = [
        MediumVulnerability(1, "GHSA-9wx4-h78v-vm56", "CVE-2024-35195", "requests", "2.31.0"),
        CriticalVulnerability(2, "PYSEC-2024-1", None, "Flask", ""),
    ]
    document = json.loads(SBOMService().generate(project, vulnerabilities).content)
    medium, critical = document["vulnerabilities"]

    assert medium["id"] == "GHSA-9wx4-h78v-vm56"
    assert medium["ratings"] == [{"severity": "medium"}]
    assert medium["affects"] == [{"ref": "pkg:pypi/requests@2.31.0"}]
    assert medium["references"][0]["id"] == "CVE-2024-35195"

    # the package name is normalized before being linked: "Flask" -> "flask"
    assert critical["ratings"] == [{"severity": "critical"}]
    assert critical["affects"] == [{"ref": "pkg:pypi/flask"}]
    assert "references" not in critical


def test_generate_vulnerability_without_osv_id_falls_back_to_cve(project, file_service):
    vulnerability = HighVulnerability(1, None, "CVE-2024-0001", "requests", "2.31.0")
    document = json.loads(SBOMService().generate(project, [vulnerability]).content)
    entry = document["vulnerabilities"][0]
    assert entry["id"] == "CVE-2024-0001"
    # the id is already the CVE, so it is not repeated in the references
    assert "references" not in entry


def test_generate_vulnerability_on_unlisted_package(project, file_service):
    """A vulnerability on a package absent from the SBOM is linked to nothing."""
    vulnerability = HighVulnerability(1, "OSV-1", None, "numpy", "1.0")
    document = json.loads(SBOMService().generate(project, [vulnerability]).content)
    assert "affects" not in document["vulnerabilities"][0]


@pytest.mark.parametrize(
    "vulnerability_class, expected",
    [
        (CriticalVulnerability, "critical"),
        (HighVulnerability, "high"),
        (MediumVulnerability, "medium"),
        (LowVulnerability, "low"),
    ],
)
def test_generate_severity_from_subclass(
    project, file_service, vulnerability_class, expected
):
    """Severity is deduced from the class, not from a text attribute."""
    vulnerability = vulnerability_class(1, "OSV-1", None, "requests", "2.31.0")
    document = json.loads(SBOMService().generate(project, [vulnerability]).content)
    assert document["vulnerabilities"][0]["ratings"] == [{"severity": expected}]


# ------------------- SBOMService.create_empty_sbom()
def test_create_empty_sbom():
    sbom = SBOMService().create_empty_sbom()
    assert isinstance(sbom, SBOMFile)
    assert sbom.name == "Empty"
    assert sbom.content == b"0"
    assert sbom.type_file == "json"
