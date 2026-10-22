from business_object.user import User
from dao.user_dao import UserDao
from utils.log_utils import log


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
            User object created or None if creation failed.
        """
        new_user = User(username=username, password=password, email=email, acces_token=None)    #Problème: comment créer le id
        return new_user if UserDao().create(new_user) else None

    @log
    def find_by_id(self, id: int) -> User:
        """
        Find a user by the id
        Args:
            id (int) : id of the user to find
        Returns:
            User that need to be found or None if search failed
        """
        return UserDao().find_by_id(id)

    @log
    def update(self, user: User) -> User:
        """
        Update a user
        Args:
            user (User) : user to update
        Returns:
            User updated
        """
        user_updated = UserDao().update(user)
        if user_updated:
            return UserDao().find_by_id(user.id_user)
        else:
            return None

    @log
    def delete(self, user: User) -> bool:
        """
        Delete a user
        Args:
            user (User) : user to delete
        Returns:
            True if delete is succesful, False otherwise
        """
        return UserDao().delete(user)

    @log
    def login (self, username: str, password: str) -> User:
        """
        Login using password and username
        Args:
            username (str) : username of the user
            password (str) : password to login
        Returns:
            User to login or None if failed
        """
        return UserDao().login(username, password)

    @log
    def username_already_used(self, username: str) -> bool:
        """
        Return if a username is already used
        Args:
            username (str) : username to verify if it is already used
        Returns:
            True if already used, False otherwise
        """
        
