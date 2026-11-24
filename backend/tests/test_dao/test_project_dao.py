from unittest.mock import MagicMock, patch

import pytest

from business_object.project import Project
from dao.project_dao import ProjectDao


@pytest.fixture
def cursor():
    with patch("dao.project_dao.DBConnection") as mock_db:
        fake_cursor = MagicMock()
        mock_db.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = fake_cursor
        yield fake_cursor


def test_create_success(cursor):
    cursor.fetchone.return_value = {"id_project": 42}
    project = MagicMock(
        name_project="My project",
        secretHMACkey=b"secret123",
        id_project=None,
    )

    result = ProjectDao().create(project, id_user=1)

    assert result is True
    assert project.id_project == 42
    assert cursor.execute.call_args.args[1] == {
        "name_project": "My project",
        "id_user": 1,
        "secretHMACkey": b"secret123",
    }


def test_create_returns_false_when_no_row(cursor):
    cursor.fetchone.return_value = None
    project = MagicMock(name_project="My project", secretHMACkey=b"secret123", id_project=None)

    assert ProjectDao().create(project, id_user=1) is False
    assert project.id_project is None


def test_create_raises_on_db_error(cursor):
    cursor.execute.side_effect = Exception("boom")
    project = MagicMock(name_project="My project", secretHMACkey=b"secret123")

    with pytest.raises(Exception, match="boom"):
        ProjectDao().create(project, id_user=1)


def test_find_by_id_found(cursor):
    cursor.fetchone.return_value = {
        "id_project": 10,
        "name_project": "My project",
        "id_user": 1,
        "secrethmackey": b"secret123",
    }

    project = ProjectDao().find_by_id(10)

    assert isinstance(project, Project)
    assert project.id_project == 10
    assert project.name_project == "My project"
    assert project.secretHMACkey == b"secret123"
    assert cursor.execute.call_args.args[1] == {"id_project": 10}


def test_find_by_id_accepts_string_secret_key(cursor):
    cursor.fetchone.return_value = {
        "id_project": 10,
        "name_project": "My project",
        "secrethmackey": "secret123",
    }

    project = ProjectDao().find_by_id(10)

    assert project.secretHMACkey == b"secret123"


def test_find_by_id_not_found(cursor):
    cursor.fetchone.return_value = None
    assert ProjectDao().find_by_id(999) is None


def test_find_by_id_raises_on_db_error(cursor):
    cursor.execute.side_effect = Exception("boom")
    with pytest.raises(Exception, match="boom"):
        ProjectDao().find_by_id(10)


def test_list_all_project_returns_projects(cursor):
    cursor.fetchall.return_value = [
        {"id_project": 10, "name_project": "Project A", "secrethmackey": b"secretA"},
        {"id_project": 11, "name_project": "Project B", "secrethmackey": b"secretB"},
    ]

    projects = ProjectDao().list_all_project(1)

    assert len(projects) == 2
    assert all(isinstance(project, Project) for project in projects)
    assert projects[0].id_project == 10
    assert projects[0].name_project == "Project A"
    assert projects[1].id_project == 11
    assert projects[1].secretHMACkey == b"secretB"
    assert cursor.execute.call_args.args[1] == {"id_user": 1}


def test_list_all_project_empty(cursor):
    cursor.fetchall.return_value = []
    assert ProjectDao().list_all_project(1) == []


def test_list_all_project_raises_on_db_error(cursor):
    cursor.execute.side_effect = Exception("boom")
    with pytest.raises(Exception, match="boom"):
        ProjectDao().list_all_project(1)


def test_update_success(cursor):
    cursor.rowcount = 1
    project = MagicMock(
        id_project=10,
        name_project="New name",
        secretHMACkey=b"secret123",
    )

    assert ProjectDao().update(project) is True
    assert cursor.execute.call_args.args[1] == {
        "name_project": "New name",
        "secretHMACkey": b"secret123",
        "id_project": 10,
    }


def test_update_project_not_found(cursor):
    cursor.rowcount = 0
    project = MagicMock(id_project=999, name_project="Missing", secretHMACkey=b"secret123")
    assert ProjectDao().update(project) is False


def test_update_raises_on_db_error(cursor):
    cursor.execute.side_effect = Exception("boom")
    project = MagicMock(id_project=10, name_project="Project", secretHMACkey=b"secret123")
    with pytest.raises(Exception, match="boom"):
        ProjectDao().update(project)


def test_delete_success(cursor):
    cursor.rowcount = 1
    project = MagicMock(id_project=10)
    assert ProjectDao().delete(project) is True
    assert cursor.execute.call_args.args[1] == {"id_project": 10}


def test_delete_project_not_found(cursor):
    cursor.rowcount = 0
    assert ProjectDao().delete(MagicMock(id_project=999)) is False


def test_delete_raises_on_db_error(cursor):
    cursor.execute.side_effect = Exception("boom")
    with pytest.raises(Exception, match="boom"):
        ProjectDao().delete(MagicMock(id_project=10))


def test_find_by_id_and_user_found(cursor):
    cursor.fetchone.return_value = {
        "id_project": 10,
        "name_project": "My project",
        "id_user": 1,
        "secrethmackey": b"secret123",
    }

    project = ProjectDao().find_by_id_and_user(10, 1)

    assert isinstance(project, Project)
    assert project.id_project == 10
    assert project.name_project == "My project"
    assert project.secretHMACkey == b"secret123"
    assert cursor.execute.call_args.args[1] == {"id_project": 10, "id_user": 1}


def test_find_by_id_and_user_not_owned(cursor):
    cursor.fetchone.return_value = None
    assert ProjectDao().find_by_id_and_user(10, 2) is None


def test_find_by_id_and_user_raises_on_db_error(cursor):
    cursor.execute.side_effect = Exception("boom")
    with pytest.raises(Exception, match="boom"):
        ProjectDao().find_by_id_and_user(10, 1)


def test_update_secret_key_success(cursor):
    cursor.rowcount = 1
    project = MagicMock(id_project=10, secretHMACkey=b"new_secret")

    assert ProjectDao().update_secret_key(project) is True
    assert cursor.execute.call_args.args[1] == {
        "secret_key": b"new_secret",
        "id_project": 10,
    }


def test_update_secret_key_project_not_found(cursor):
    cursor.rowcount = 0
    project = MagicMock(id_project=999, secretHMACkey=b"new_secret")
    assert ProjectDao().update_secret_key(project) is False


def test_update_secret_key_raises_on_db_error(cursor):
    cursor.execute.side_effect = Exception("boom")
    project = MagicMock(id_project=10, secretHMACkey=b"new_secret")
    with pytest.raises(Exception, match="boom"):
        ProjectDao().update_secret_key(project)
