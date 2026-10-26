from unittest.mock import MagicMock, patch

import pytest

from business_object.user import User
from dao.user_dao import UserDao

# - TESTS DE CREATE ----------------------


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

# - TESTS DE FIND_BY_ID ----------------------


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
