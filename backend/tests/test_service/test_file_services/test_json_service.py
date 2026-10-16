import pytest

# from datetime import datetime
from src.service.file_services.json_service import JsonService

# from src.business_object.dependency import Dependency


def test_parse_dependencies_json_merges_dependencies_and_dev():
    # GIVEN
    content = b'{"dependencies": {"express": "^4.0.0"}, "devDependencies": {"jest": "^29.0.0"}}'
    list_result = [("express", "^4.0.0"), ("jest", "^29.0.0")]

    # WHEN
    list_dep = JsonService().parse_dependencies(content)

    # THEN
    for i in range(len(list_dep)):
        assert list_dep[i].name == list_result[i][0]
        assert list_dep[i].version == list_result[i][1]


def test_parse_dependencies_json_without_dependencies():
    # GIVEN
    content = b'{"name": "x"}'
    list_result = []

    # WHEN
    list_dep = JsonService().parse_dependencies(content)

    # THEN
    assert list_dep == list_result


def test_parse_dependencies_json_invalid_raises():
    # GIVEN
    content = b"{pas du json"

    # THEN
    with pytest.raises(ValueError):  # JSONDecodeError hérite de ValueError
        JsonService().parse_dependencies(content)
