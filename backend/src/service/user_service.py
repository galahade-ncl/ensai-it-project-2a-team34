from business_object.user import User
from dao.user_dao import UserDao

class UserService:
    """
    Service that handles business logic related to a user
    """
    @log
    def create (self, username: str, password: str, email: str) -> User:
        """
        Create a new user in the system.
        Args:
            username (str) : name of the user
            password (str) : password of the user
            email (str) : email of the user
        Returns:
            User object created of None if creation failed.
        """
        new_user = User(id_user= , username=username, password=password, email=email, acces_token=None)
        return new_user if UserDao().create(new_user) else None

    @log
    def find_by_id(self, id: int) -> User:
        