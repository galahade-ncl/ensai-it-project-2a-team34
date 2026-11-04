import json
from types import SimpleNamespace

import pytest

from business_object.file.sbomfile import SBOMFile
from business_object.vulnerability.critical_vulnerability import CriticalVulnerability
from business_object.vulnerability.high_vulnerability import HighVulnerability
from business_object.vulnerability.low_vulnerability import LowVulnerability
from business_object.vulnerability.medium_vulnerability import MediumVulnerability
from service.sbom_service import SBOMService

# A tester SBOMService.generate() et SBOMfile.get_duty()


# fixture
@pytest.fixture
def user():
    """fictive user because project need a constructor user"""
    return SimpleNamespace(
        id_user=1, username="Jean-Michel", email="jean-michel@mail.fr", password="0000"
    )


@pytest.fixture
def project():
    """fictive project"""
    dependency_file = SimpleNamespace(
        name="requirements.txt",
        content=b"requests==2.31.0\nDjango_REST.framework==3.15.1\npandas>=2.0\nflask\n# comment\n\n-r dev.txt\n",
    )
    return SimpleNamespace(
        id_project=1,
        name_project="demo",
        user=user,
        secretHMACkey=bytes.fromhex(
            "7f2cd2cada12a1c7f6550f4b9aa3873776d6b0228b2d9c1596dcdf8eda301930"
        ),
        dependencyfile=dependency_file,
    )


def test_generate_successful(project):
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


def test_generate_with_given_dependencies(project):
    sbom = SBOMService().generate(project, dependencies=["numpy==1.26.4", "numpy==1.26.4"])
    assert len(json.loads(sbom.content)["components"]) == 1


def test_generate_npm():
    """Production of npm purl"""
    project = SimpleNamespace(
        name_project="front",
        user=user,
        secretHMACkey=bytes.fromhex(
            "36ae536d5635a5ed214da489269b91dc9b9d4b97db9c077bd66830b54208329d"
        ),
        dependencyfile=SimpleNamespace(name="package.json", content=b""),
    )
    sbom = SBOMService().generate(project, dependencies=["react@18.3.1", "@types/node@20.1.0"])
    purls = [c["purl"] for c in json.loads(sbom.content)["components"]]
    assert purls == ["pkg:npm/react@18.3.1", "pkg:npm/@types/node@20.1.0"]


def test_generate_with_vulnerabilities(project):
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
def test_generate_severity_from_subclass(project, vulnerability_class, expected):
    vulnerability = vulnerability_class(1, "OSV-1", None, "requests", "2.31.0")
    document = json.loads(SBOMService().generate(project, vulnerabilities=[vulnerability]).content)
    assert document["vulnerabilities"][0]["ratings"] == [{"severity": expected}]
