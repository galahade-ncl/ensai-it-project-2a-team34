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


