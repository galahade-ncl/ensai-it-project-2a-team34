from unittest.mock import MagicMock, patch

import pytest

from business_object.user import User
from dao.user_dao import UserDao

# - TESTS OF CREATE ----------------------


def test_create_success():
    with patch("dao.user_dao.DBConnection") as mock_db:
        cursor = MagicMock()
        mock_db.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = cursor
        cursor.fetchone.return_value = {"id_user": 42}

        user = MagicMock(username="alice", password="pw", email="a@a.fr")
        result = UserDao().create(user)

    assert result is True
    assert user.id_user == 42


def test_create_returns_false_when_no_row(cursor):
    """
    Tests create when the database returns no id
    """
    cursor.fetchone.return_value = None
    user = MagicMock(username="alice", password="pw", email="a@a.fr")

    result = UserDao().create(user)

    assert result is False


def test_create_raises_on_db_error(cursor):
    """
    Tests if the error is raised on when the insertion fails
    """
    cursor.execute.side_effect = Exception("boom")
    user = MagicMock(username="alice", password="pw", email="a@a.fr")

    with pytest.raises(Exception, match="boom"):
        UserDao().create(user)


# - TESTS OF HASH_PW / VERIFY_PW ----------------------


def test_hash_pw_does_not_store_plain_password():
    """
    The hash is different from the password and is accepted by verify_pw
    """
    hashed = UserDao.hash_pw("my_password")

    assert hashed != "my_password"
    assert UserDao.verify_pw("my_password", hashed) is True


def test_hash_pw_uses_a_salt():
    """
    Two hashes of the same password are different
    """
    assert UserDao.hash_pw("my_password") != UserDao.hash_pw("my_password")


def test_verify_pw_wrong_password():
    """
    A wrong password is rejected
    """
    hashed = UserDao.hash_pw("my_password")

    assert UserDao.verify_pw("wrong_password", hashed) is False


def test_verify_pw_malformed_hash():
    """
    A malformed hash returns False instead of raising
    """
    assert UserDao.verify_pw("my_password", "not_a_bcrypt_hash") is False


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
        {
            "id_user": 1,
            "username": "alice",
            "password": "pw1",
            "email": "alice@email.com",
        },
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
    params = cursor.execute.call_args[0][1]
    assert UserDao.verify_pw("pw", params["password"])
    assert params["username"] == "alice"
    assert params["email"] == "alice@email.com"
    assert params["access_token"] == "token123"
    assert params["id_user"] == 1


def test_update_access_token_success(cursor):
    """
    Only the access token is written, for the given user
    """
    cursor.rowcount = 1

    assert UserDao().update_access_token(1, "token123") is True

    assert cursor.execute.call_args[0][1] == {"access_token": "token123", "id_user": 1}


def test_update_access_token_user_not_found(cursor):
    """
    Tests update_access_token when the user does not exist
    """
    cursor.rowcount = 0

    assert UserDao().update_access_token(999, "token123") is False


def test_update_access_token_raises_on_db_error(cursor):
    """
    Tests if the error is raised on when the update fails
    """
    cursor.execute.side_effect = Exception("boom")

    with pytest.raises(Exception, match="boom"):
        UserDao().update_access_token(1, "token123")


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
    user = MagicMock(
        id_user=1,
        username="alice",
        password="pw",
        email="alice@email.com",
        access_token=None,
    )

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


# - TESTS OF LOGIN ----------------------


def test_login_success(cursor):
    """
    The user succeds to login
    """
    cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "alice",
        "password": UserDao.hash_pw("pw"),
        "email": "alice@example.com",
        "access_token": "token123",
    }

    user = UserDao().login("alice", "pw")

    assert isinstance(user, User)
    assert user.id_user == 1
    assert user.username == "alice"
    assert user.access_token == "token123"
    # The second argument of execute() contains the request parameters
    assert cursor.execute.call_args[0][1] == {"username": "alice"}


def test_login_wrong_password(cursor):
    """
    The stored hash does not match the given password, so login fails
    """
    cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "alice",
        "password": UserDao.hash_pw("pw"),
        "email": "alice@example.com",
        "access_token": "token123",
    }

    user = UserDao().login("alice", "wrong_pw")

    assert user is None


def test_login_wrong_credentials(cursor):
    """
    The passeword is wrong so login fails
    """
    cursor.fetchone.return_value = None

    user = UserDao().login("alice", "wrong_pw")

    assert user is None


def test_login_raises_on_db_error(cursor):
    """
    An error is raised on
    """
    cursor.execute.side_effect = Exception("boom")

    with pytest.raises(Exception, match="boom"):
        UserDao().login("alice", "pw")


# - TESTS OF FIND_BY_TOKEN ----------------------


@pytest.mark.parametrize("token", [None, ""])
def test_find_by_token_empty_token(cursor, token):
    """
    Tests if it finds no user when token is None.
    """
    user = UserDao().find_by_token(token)

    assert user is None
    # No request should be send
    cursor.execute.assert_not_called()


def test_find_by_token_found(cursor):
    """
    Tests when the token is found (here token123).
    """
    cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "alice",
        "password": "pw",
        "email": "alice@example.com",
        "access_token": "token123",
    }

    user = UserDao().find_by_token("token123")

    assert isinstance(user, User)
    assert user.id_user == 1
    assert user.username == "alice"
    assert user.access_token == "token123"
    # The second argument of execute() contains the request parameters
    assert cursor.execute.call_args[0][1] == {"token": "token123"}


def test_find_by_token_not_found(cursor):
    """
    Tests when the user isn't found because the token doesn't exists.
    """
    cursor.fetchone.return_value = None

    user = UserDao().find_by_token("unknown_token")

    assert user is None


def test_find_by_token_raises_on_db_error(cursor):
    """
    Tests if the error is raised on.
    """
    cursor.execute.side_effect = Exception("boom")

    with pytest.raises(Exception, match="boom"):
        UserDao().find_by_token("token123")


# - TESTS OF FIND_BY_USERNAME ----------------------


def test_find_by_username_found(cursor):
    """
    Tests when the username exists
    """
    cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "alice",
        "password": "hashed_pw",
        "email": "alice@example.com",
    }

    user = UserDao().find_by_username("alice")

    assert isinstance(user, User)
    assert user.id_user == 1
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    # The second argument of execute() contains the request parameters
    assert cursor.execute.call_args[0][1] == {"username": "alice"}


def test_find_by_username_not_found(cursor):
    """
    Tests when the username doesn't exist
    """
    cursor.fetchone.return_value = None

    assert UserDao().find_by_username("nobody") is None


def test_find_by_username_raises_on_db_error(cursor):
    """
    Tests if the error is raised on
    """
    cursor.execute.side_effect = Exception("boom")

    with pytest.raises(Exception, match="boom"):
        UserDao().find_by_username("alice")
