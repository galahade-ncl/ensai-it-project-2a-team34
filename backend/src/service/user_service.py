import secrets

from business_object.project import Project
from business_object.user import User
from dao.project_dao import ProjectDao
from dao.user_dao import UserDao
from utils.log_utils import log


class UserService:
    """
    Service that handles business logic related to a user
    """
    @log
    def create(self, username: str, password: str, email: str) -> User | None:
        """
        Create a new user in the system.

        Parameters
        ----------
        username : str
            Name of the user.
        password : str
            Password of the user.
        email : str
            Email of the user.

        Returns
        -------
        User or None
            The created user, or None if the creation failed.
        """
        new_user = User(
            username=username,
            password=UserDao.hash_pssw(password),
            email=email,
            access_token=None
            )
        return new_user if UserDao().create(new_user) else None

    @log
    def find_by_id(self, id: int) -> User | None:
        """
        Find a user by their identifier.

        Parameters
        ----------
        id : int
            Identifier of the user to find.

        Returns
        -------
        User or None
            The user found, or None if the search failed.
        """
        return UserDao().find_by_id(id)

    @log
    def update(self, user: User) -> User | None:
        """
        Update a user.

        Parameters
        ----------
        user : User
            User to update.

        Returns
        -------
        User or None
            The updated user, or None if the update failed.
        """
        user_updated = UserDao().update(user)
        if user_updated:
            return user
        else:
            return None

    @log
    def delete(self, user: User) -> bool:
        """
        Delete a user.

        Parameters
        ----------
        user : User
            User to delete.

        Returns
        -------
        bool
            True if the deletion is successful, False otherwise.
        """
        return UserDao().delete(user)

    @log
    def login(self, username: str, password: str) -> User | None:
        """
        Log a user in with their username and password.

        A new access token is generated and stored for the user.

        Parameters
        ----------
        username : str
            Username of the user.
        password : str
            Password of the user.

        Returns
        -------
        User or None
            The logged in user with their access token, or None if the
            credentials are invalid.
        """
        user = UserDao().login(username, password)
        if user:
            # Generate a token and update the User
            user.access_token = secrets.token_urlsafe(32)
            self.update(user)
            return user
        return None

    @log
    def username_already_used(self, username: str) -> bool:
        """
        Check whether a username is already used.

        Parameters
        ----------
        username : str
            Username to check.

        Returns
        -------
        bool
            True if the username is already used, False otherwise.
        """
        return (UserDao().find_by_username(username) is not None)

    @log
    def list_all_project(self, id_user: int) -> list[Project] | None:
        """
        List all the projects owned by a user.

        Parameters
        ----------
        id_user : int
            Identifier of the user.

        Returns
        -------
        list of Project or None
            Projects owned by the user, or None if the user does not exist.
        """
        # Find the user corresponding to the id
        user = UserService().find_by_id(id_user)
        if not user:
            return None
        return ProjectDao().list_all_project(id_user)
