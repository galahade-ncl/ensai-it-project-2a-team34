# import pytest
# from datetime import datetime
from src.service.file_services.txt_service import TxtService

# from src.business_object.dependency import Dependency


def test_parse_dependencies_txt_parse_pinned_and_unpinned():
    # GIVEN
    content = b"requests==2.31.0\nflask\n"
    list_result = [("requests", "2.31.0"), ("flask", None)]

    # WHEN
    list_dep = TxtService().parse_dependencies(content)

    # THEN
    for i in range(len(list_dep)):
        assert list_dep[i].name == list_result[i][0]
        assert list_dep[i].version == list_result[i][1]


def test_parse_dependencies_txt_ignores_comments_options_and_blank_lines():
    # GIVEN
    content = b"# commentaire\n\n-r other.txt\nrequests==2.0  # inline\n"
    list_result = [("requests", "2.0")]

    # WHEN
    list_dep = TxtService().parse_dependencies(content)

    # THEN
    for i in range(len(list_dep)):
        assert list_dep[i].name == list_result[i][0]
        assert list_dep[i].version == list_result[i][1]


def test_parse_dependencies_txt_handles_bom():
    # GIVEN
    content = b"\xef\xbb\xbfrequests==1.0"
    list_result = [("requests", "1.0")]

    # WHEN
    list_dep = TxtService().parse_dependencies(content)

    # THEN
    for i in range(len(list_dep)):
        assert list_dep[i].name == list_result[i][0]
        assert list_dep[i].version == list_result[i][1]


def test_parse_dependencies_txt_empty():
    # GIVEN
    content = b""
    list_result = []

    # WHEN
    list_dep = TxtService().parse_dependencies(content)

    # THEN
    assert list_dep == list_result
