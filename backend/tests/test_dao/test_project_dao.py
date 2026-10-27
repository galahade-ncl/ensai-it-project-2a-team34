from unittest.mock import MagicMock, patch

import pytest

from business_object.project import Project
from dao.project_dao import ProjectDao


@pytest.fixture
def cursor():
    """
    Gives a fake cursor for the tests.
    """
    with patch("dao.project_dao.DBConnection") as mock_db:
        fake_cursor = MagicMock()
        mock_db.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = fake_cursor
        yield fake_cursor


# - TESTS OF CREATE ----------------------


def test_create_success(cursor):
    """
    Tests if the project is well created.
    """
    cursor.fetchone.return_value = {"id_project": 42}
    project = MagicMock(
        name_project="Mon projet",
        user=MagicMock(id_user=1),
        secretHMACkey="secret123",
        id_project=None,
    )

    result = ProjectDao().create(project)

    assert result is True
    assert project.id_project == 42
    # The second argument of execute() contains the request parameters
    assert cursor.execute.call_args[0][1] == {
        "name_project": "Mon projet",
        "id_user": 1,
        "secretHMACkey": "secret123",
    }


def test_create_returns_false_when_no_row(cursor):
    """
    Tests when the base returns nothing (nothing was created).
    """
    cursor.fetchone.return_value = None
    project = MagicMock(
        name_project="Mon projet",
        user=MagicMock(id_user=1),
        secretHMACkey="secret123",
        id_project=None,
    )

    result = ProjectDao().create(project)

    assert result is False
    assert project.id_project is None


def test_create_raises_on_db_error(cursor):
    """
    Tests if the error is raised on
    """
    cursor.execute.side_effect = Exception("boom")
    project = MagicMock(user=MagicMock(id_user=1))

    with pytest.raises(Exception, match="boom"):
        ProjectDao().create(project)
