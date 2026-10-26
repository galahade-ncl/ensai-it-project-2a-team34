from unittest.mock import MagicMock, patch

import pytest

from business_object.user import User
from dao.user_dao import UserDao

# - TESTS OF CREATE ----------------------


def test_create_success():
    with patch("dao.user_dao.DBConnection") as mock_db:
        cursor = MagicMock()
        mock_db.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = (
            cursor
        )
        cursor.fetchone.return_value = {"id_user": 42}

        user = MagicMock(username="alice", password="pw", email="a@a.fr")
        result = UserDao().create(user)

    assert result is True
    assert user.id_user == 42


# - TESTS OF FIND_BY_ID ----------------------


@pytest.fixture
def cursor():
    """Gives a fake cursor (a mock one)"""
    with patch("dao.user_dao.DBConnection") as mock_db:
        fake_cursor = MagicMock()
        mock_db.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = fake_cursor
        yield fake_cursor


def test_find_by_id_found(cursor):
    """
    Test if there is a user for this id and we found the good one
    """
    cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "alice",
        "password": "pw",
        "email": "alice@email.com",
    }

    user = UserDao().find_by_id(1)

    assert isinstance(user, User)
    assert user.id_user == 1
    assert user.username == "alice"
    assert user.email == "alice@email.com"
    # The second argument of execute() contains the request parameters
    assert cursor.execute.call_args[0][1] == {"id_user": 1}


def test_find_by_id_not_found(cursor):
    """
    Test if there is no user for this id
    """
    cursor.fetchone.return_value = None

    user = UserDao().find_by_id(999)

    assert user is None


def test_find_by_id_raises_on_db_error(cursor):
    """
    Test if the fictive error boom is raised on as an exception
    """
    cursor.execute.side_effect = Exception("boom")

    with pytest.raises(Exception, match="boom"):
        UserDao().find_by_id(1)


# - TESTS OF FIND_ALL ----------------------


def test_find_all_found(cursor):
    """
    Test if there are users and we found the good ones
    """
    cursor.fetchall.return_value = [
        {"id_user": 1, "username": "alice", "password": "pw1", "email": "alice@email.com"},
        {"id_user": 2, "username": "bob", "password": "pw2", "email": "bob@email.com"},
    ]

    users = UserDao().find_all()

    assert len(users) == 2
    assert isinstance(users[0], User)
    assert isinstance(users[1], User)
    assert users[0].id_user == 1
    assert users[0].username == "alice"
    assert users[0].email == "alice@email.com"
    assert users[1].id_user == 2
    assert users[1].username == "bob"
    assert users[1].email == "bob@email.com"


def test_find_all_empty(cursor):
    """
    Test if there is no user
    """
    cursor.fetchall.return_value = []

    users = UserDao().find_all()

    assert users == []


def test_find_all_raises_on_db_error(cursor):
    """
    Test if the fictive error boom is raised on as an exception
    """
    cursor.execute.side_effect = Exception("boom")

    with pytest.raises(Exception, match="boom"):
        UserDao().find_all()


# - TESTS OF UPDATE ----------------------


def test_update_success(cursor):
    """
    Tests update when it must succed
    """
    cursor.rowcount = 1
    user = MagicMock(
        id_user=1,
        username="alice",
        password="pw",
        email="alice@email.com",
        access_token="token123",
    )

    result = UserDao().update(user)

    assert result is True
    # The second argument of execute() contains the request parameters
    assert cursor.execute.call_args[0][1] == {
        "username": "alice",
        "password": "pw",
        "email": "alice@email.com",
        "access_token": "token123",
        "id_user": 1,
    }


def test_update_user_not_found(cursor):
    """
    Tests update when it must fail
    """
    cursor.rowcount = 0
    user = MagicMock(
        id_user=999,
        username="nobody",
        password="pw",
        email="nobody@email.com",
        access_token=None,
    )

    result = UserDao().update(user)

    assert result is False


def test_update_raises_on_db_error(cursor):
    """
    Tests update when it must raise on an exception error
    """
    cursor.execute.side_effect = Exception("boom")
    user = MagicMock(id_user=1)

    with pytest.raises(Exception, match="boom"):
        UserDao().update(user)


# - TESTS OF DELETE ----------------------

def test_delete_success(cursor):
    """
    Tests if the user is correctly deleted
    """
    cursor.rowcount = 1
    user = MagicMock(id_user=1)

    result = UserDao().delete(user)

    assert result is True
    # The second argument of execute() contains the request parameters
    assert cursor.execute.call_args[0][1] == {"id_user": 1}


def test_delete_user_not_found(cursor):
    """
    Tests if the user isn't deleted because not found
    """
    cursor.rowcount = 0
    user = MagicMock(id_user=999)

    result = UserDao().delete(user)

    assert result is False


def test_delete_raises_on_db_error(cursor):
    """
    Tests if an error is raised on.
    """
    cursor.execute.side_effect = Exception("boom")
    user = MagicMock(id_user=1)

    with pytest.raises(Exception, match="boom"):
        UserDao().delete(user)
