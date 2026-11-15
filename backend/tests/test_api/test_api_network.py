import pytest

from api_deps_dev.api_deps_dev import API_DEPSDEV
from api_osv.api_osv import API_OSV
from business_object.dependency import Dependency

pytestmark = pytest.mark.network  # marque tous les tests du fichier


def test_osv_real_call():
    dep = Dependency(id_dependency=1, name="requests", version="2.19.0")
    result = API_OSV.find_vulnerabilities(dep, "PyPI")
    assert len(result) > 0  # requests 2.19.0 a des vulnérabilités connues


def test_depsdev_real_call():
    dep = Dependency(id_dependency=1, name="requests", version="2.31.0")
    result = API_DEPSDEV.find_licences(dep, "PyPI")
    assert len(result) > 0
    assert any(lic.name == "Apache-2.0" for lic in result)
