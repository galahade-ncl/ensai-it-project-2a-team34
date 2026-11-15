from unittest.mock import MagicMock, patch

import pytest
import requests

from api_deps_dev.api_deps_dev import (
    API_DEPSDEV,
    DEFAULT_RISK,
    DEPSDEV_URL,
    LICENCE_RISK,
)
from business_object.dependency import Dependency

MODULE = "api_deps_dev.api_deps_dev"


def make_response(data=None, status_code=200) -> MagicMock:
    """Fake requests.Response."""
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = data if data is not None else {}
    return response


def dep(name="requests", version="2.19.0") -> Dependency:
    return Dependency(id_dependency=1, name=name, version=version)


class TestCleanVersion:
    @pytest.mark.parametrize(
        "raw, expected",
        [
            ("1.2.3", "1.2.3"),
            ("^1.2.0", "1.2.0"),
            ("~1.2.0", "1.2.0"),
            (">=1.0,<2", "1.0"),
            ("==2.19.0", "2.19.0"),
            ("~=1.4.2", "1.4.2"),
            ("2.0.0rc1", "2.0.0rc1"),
            ("1.0.0-beta.1", "1.0.0-beta.1"),
            ("v1.2.3", "1.2.3"),
            ("1", "1"),
        ],
    )
    def test_extracts_first_version(self, raw, expected):
        assert API_DEPSDEV.clean_version(raw) == expected

    @pytest.mark.parametrize("raw", [None, "", "*", "latest", "abc"])
    def test_returns_none_without_version(self, raw):
        assert API_DEPSDEV.clean_version(raw) is None


class TestToLicences:
    @pytest.mark.parametrize("name, risk", list(LICENCE_RISK.items()))
    def test_known_licences_get_their_risk(self, name, risk):
        result = API_DEPSDEV._to_licences([name])
        assert result[0].name == name
        assert result[0].risk_level == risk

    def test_unknown_licence_gets_default_risk(self):
        result = API_DEPSDEV._to_licences(["Proprietary-Foo"])
        assert result[0].risk_level == DEFAULT_RISK == "unknown"

    def test_empty_list(self):
        assert API_DEPSDEV._to_licences([]) == []

    def test_keeps_order_and_mixes_known_and_unknown(self):
        result = API_DEPSDEV._to_licences(["MIT", "WTFPL", "GPL-3.0"])
        assert [(lic.name, lic.risk_level) for lic in result] == [
            ("MIT", "low"),
            ("WTFPL", "unknown"),
            ("GPL-3.0", "high"),
        ]


class TestDefaultVersion:
    base = f"{DEPSDEV_URL}/systems/PYPI/packages/requests"

    def test_returns_default_version(self):
        data = {
            "versions": [
                {"versionKey": {"version": "2.0.0"}},
                {"versionKey": {"version": "2.31.0"}, "isDefault": True},
            ]
        }
        with patch(f"{MODULE}.requests.get", MagicMock(return_value=make_response(data))):
            assert API_DEPSDEV._default_version(self.base) == "2.31.0"

    def test_no_default_version_flagged(self):
        data = {"versions": [{"versionKey": {"version": "1.0.0"}}]}
        with patch(f"{MODULE}.requests.get", MagicMock(return_value=make_response(data))):
            assert API_DEPSDEV._default_version(self.base) is None

    def test_no_versions_key(self):
        with patch(f"{MODULE}.requests.get", MagicMock(return_value=make_response({}))):
            assert API_DEPSDEV._default_version(self.base) is None

    def test_unknown_package_returns_none(self):
        get = MagicMock(return_value=make_response(status_code=404))
        with patch(f"{MODULE}.requests.get", get):
            assert API_DEPSDEV._default_version(self.base) is None

    def test_http_error_is_propagated(self):
        response = make_response(status_code=500)
        response.raise_for_status.side_effect = requests.HTTPError("500")
        with patch(f"{MODULE}.requests.get", MagicMock(return_value=response)):
            with pytest.raises(requests.HTTPError):
                API_DEPSDEV._default_version(self.base)

    def test_calls_base_url_with_timeout(self):
        get = MagicMock(return_value=make_response({}))
        with patch(f"{MODULE}.requests.get", get):
            API_DEPSDEV._default_version(self.base)
