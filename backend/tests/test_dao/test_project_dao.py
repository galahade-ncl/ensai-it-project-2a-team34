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
        name_project="My projet",
        user=MagicMock(id_user=1),
        secretHMACkey="secret123",
        id_project=None,
    )

    result = ProjectDao().create(project)

    assert result is True
    assert project.id_project == 42
    # The second argument of execute() contains the request parameters
    assert cursor.execute.call_args[0][1] == {
        "name_project": "My projet",
        "id_user": 1,
        "secretHMACkey": "secret123",
    }


def test_create_returns_false_when_no_row(cursor):
    """
    Tests when the base returns nothing (nothing was created).
    """
    cursor.fetchone.return_value = None
    project = MagicMock(
        name_project="My project",
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


# - TESTS OF FIND_BY_ID ----------------------


@pytest.fixture
def user_dao():
    """
    Replace UserDao by a fake for the tests.
    """
    with patch("dao.project_dao.UserDao") as mock_user_dao:
        yield mock_user_dao.return_value


def test_find_by_id_found(cursor, user_dao):
    """
    Tests when the project is found.
    """
    fake_user = MagicMock(id_user=1)
    user_dao.find_by_id.return_value = fake_user
    cursor.fetchone.return_value = {
        "id_project": 10,
        "name_project": "My project",
        "id_user": 1,
        "secrethmackey": "secret123",
    }

    project = ProjectDao().find_by_id(10)

    assert isinstance(project, Project)
    assert project.id_project == 10
    assert project.name_project == "My project"
    assert project.user == fake_user
    assert project.secretHMACkey == "secret123"
    # The second argument of execute() contains the request parameters
    assert cursor.execute.call_args[0][1] == {"id_project": 10}
    # The owner was search with the id_user of the line
    user_dao.find_by_id.assert_called_once_with(1)


def test_find_by_id_not_found(cursor, user_dao):
    """
    Tests when the project isn't found.
    """
    cursor.fetchone.return_value = None

    project = ProjectDao().find_by_id(999)

    assert project is None
    # There is no project so we don't search a user
    user_dao.find_by_id.assert_not_called()


def test_find_by_id_raises_on_db_error(cursor, user_dao):
    """
    Tests when an error is raised on.
    """
    cursor.execute.side_effect = Exception("boom")

    with pytest.raises(Exception, match="boom"):
        ProjectDao().find_by_id(10)


# - TESTS OF LIST_ALL_PROJECT ----------------------


def test_list_all_project_returns_projects(cursor):
    """
    Tests when the methods returns projects.
    """
    user = MagicMock(id_user=1)
    cursor.fetchall.return_value = [
        {"id_project": 10, "name_project": "Projet A", "secrethmackey": "secretA"},
        {"id_project": 11, "name_project": "Projet B", "secrethmackey": "secretB"},
    ]

    projects = ProjectDao().list_all_project(user)

    assert len(projects) == 2
    assert all(isinstance(p, Project) for p in projects)
    assert projects[0].id_project == 10
    assert projects[0].name_project == "Projet A"
    assert projects[1].id_project == 11
    assert projects[1].secretHMACkey == "secretB"
    # All projects are owned by the user gived as an argument (here id_user = 1)
    assert all(p.user == user for p in projects)
    # The second argument of execute() contains the request parameters
    assert cursor.execute.call_args[0][1] == {"id_user": 1}


def test_list_all_project_empty(cursor):
    """
    Tests when the user does,'t have any project.
    """
    user = MagicMock(id_user=1)
    cursor.fetchall.return_value = []

    projects = ProjectDao().list_all_project(user)

    assert projects == []


def test_list_all_project_raises_on_db_error(cursor):
    """
    Tests when an error is raised on.
    """
    user = MagicMock(id_user=1)
    cursor.execute.side_effect = Exception("boom")

    with pytest.raises(Exception, match="boom"):
        ProjectDao().list_all_project(user)
