from unittest.mock import MagicMock

from src.business_object.user import User
from src.service.user_service import UserService
from src.dao.user_dao import UserDao

userlist = [
    User(
        username="Annabelle",
        password="0123456789",
        email="annabelle@example.com"
    ),
    User(
        username="Madie",
        password="9876543210",
        email="madie@example.com"
    ),
    User(
        username="Galahade",
        password="112233445566778899",
        email= "galahade@example.com"
    )
]

def test_created_successful():
    """Successfully created a User"""

    # GIVEN
    username, password, email = "Annabelle", "123456789", "annabelle@example.com"
    UserDao().create = MagicMock(return_value=True)

    # WHEN
    user = UserService().create(username, password, email)

    # THEN
    assert user.username == username

def test_create_failed():
    """Failed to create a User because UserDao().create returns False"""

    # GIVEN
    username, password, email = "Annabelle", "123456789", "annabelle@example.com"
    UserDao().create = MagicMock(return_value=False)

    # WHEN
    user = UserService().create(username, password, email)

    # THEN
    assert user is None

    
