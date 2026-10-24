from unittest.mock import MagicMock

import pytest
from src.business_object.user import User
from src.dao.user_dao import UserDao
from src.service.user_service import UserService


@pytest.mark.parametrize(
    "id_user, username, password, email",
    [
        (1,"Annabelle","0123456789","annabelle@example.com"),
        (2, "Madie", "9876543210", "madie@example.com"),
        (3, "Galahade", "112233445566778899", "galahade@example.com"),
    ],
)


def test_created_successful():
    """Successfully created a User"""

    # GIVEN
    user = User(id_user=1, username="Jean", password="123456789", email="jean@example.com")
    UserDao().create = MagicMock(return_value=True)

    # WHEN
    user = UserService().create(username, password, email)

    # THEN
    assert user.username == username

def test_create_failed(id_user, username, password, email):
    """Failed to create a User because UserDao().create returns False"""

    # GIVEN
    user = User(id_user=id_user, username=username, password=password, email=email)
    UserDao().create = MagicMock(return_value=False)

    # WHEN
    user = UserService().create(username, password, email)

    # THEN
    assert user is None

def test_find_by_id_successful(id_user, username, password, email):
    """Successfully find the user"""

    # GIVEN
    user = User(id_user=id_user, username=username, password=password, email=email)
    UserDao().find_by_id = MagicMock(return_value=user)

    # WHEN
    res = UserService().find_by_id(id_user)

    # THEN
    assert res == user

def test_find_by_id_failed(id_user, username, password, email):
    """Fail to find the user"""

    # GIVEN
    UserDao().find_by_id = MagicMock(return_value=None)

    # WHEN
    res = UserService().find_by_id(555)

    # THEN
    assert res is None

def test_update_successful(id_user, username, password, email):
    """Successfully update a user"""

    # GIVEN
    updated_user = User(id_user=id_user, username=username, password=password, email=email)
    user = User(id_user=id_user, username=username, password=password, email=email)
    UserDao().update = MagicMock(return_value=True)
    UserDao.find_by_id = MagicMock(return_value=updated_user)

    # WHEN
    res = UserService().update(user)

    # THEN
    assert res == updated_user
    UserDao.update.assert_called_once_with(user)
    UserDao.find_by_id.assert_called_once_with(user.id_user)


def test_update_failed(id_user, username, password, email):
    """Fail to update a user because UserDao().update returns False"""

    # GIVEN
    user = User(id_user=id_user, username=username, password=password, email=email)
    UserDao.update = MagicMock(return_value=None)

    # WHEN
    result = UserService().update(user)

    # THEN
    assert result is None
    UserDao.find_by_id.assert_not_called()

def test_delete_successful(id_user, username, password, email):
    """Successfully delete a user"""

    # GIVEN
    user = User(id_user=id_user, username=username, password=password, email=email)
    UserDao().delete = MagicMock(return_value=True)

   # WHEN
    res = UserService().delete(user)

    # THEN
    assert res is True
    UserDao.delete.assert_called_once_with(user)


def test_delete_failed(id_user, username, password, email):
    """Fail to delete a user because UserDao().delete returns False"""

    # GIVEN
    user = User(id_user=id_user, username=username, password=password, email=email)
    UserDao.delete = MagicMock(return_value=False)

    # WHEN
    res = UserService().delete(user)

    # THEN
    assert res is False

def test_login_successful(id_user, username, password, email):
    """Successfully login with a valid username and password"""

    # GIVEN
    user = User(id_user=id_user, username=username, password=password, email=email)
    UserDao().login = MagicMock(return_value=user)

    # WHEN
    res = UserService().login(username, password)

    # THEN
    assert res == user
    UserDao.login.call_count == 1

def test_login_failed(id_user, username, password, email):
    """Fail to login because credentials are wrong"""

    # GIVEN
    UserDao.login = MagicMock(return_value=None)

    # WHEN
    res = UserService().login(username, "wrong_password")

    # THEN
    assert res is None

def test_username_already_used_true(id_user, username, password, email):
    """Return True when a user with this username already exists"""

    # GIVEN
    user = User(id_user=id_user, username=username, password=password, email=email)
    UserDao.find_by_username = MagicMock(return_value=user)

    # WHEN
    res = UserService().username_already_used(username)

    # THEN
    assert res is True
    UserDao.find_by_username.assert_called_once_with(username)


def test_username_already_used_false():
    """Return False when no user has this username"""

    # GIVEN
    UserDao().find_by_username = MagicMock(return_value=None)

    # WHEN
    res = UserService().username_already_used("SArah")

    # THEN
    assert res is False
