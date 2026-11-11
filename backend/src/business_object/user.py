class User:
    """
    Class modelling a user.

    Attributes
    ----------
    id_user : int or None
        Unique identifier of the user.
    username : str
        Name of the user.
    password : str
        Password of the user.
    email : str
        Email of the user.
    access_token : str or None
        Access token of the user (optional).

    Methods
    -------
    __str__()
        Return an informal string representation of the user.
    __eq__(other)
        Return True if the compared users have the same identifier.
    __hash__()
        Return a hash of the user identifier, allowing users to be used
        in a set or as dict keys.
    """
    def __init__(self, username, password, email, id_user=None, access_token=None) -> None:
        self.id_user = id_user
        self.username = username
        self.password = password
        self.email = email
        self.access_token = access_token

    def __str__(self) -> str:
        """
        Return an informal string representation of the user.

        Returns
        -------
        str
            String showing the username, the identifier and the email
            of the user.
        """
        return f"{self.username} (id :{self.id_user}, email : {self.email})"

    def __eq__(self, other) -> bool:
        """
        Compare the user with another object.

        Two users are considered equal if they have the same identifier.

        Parameters
        ----------
        other : object
            Object to compare with.

        Returns
        -------
        bool
            True if ``other`` is a User with the same identifier, False
            otherwise. ``NotImplemented`` is returned if ``other`` is not
            a User.
        """
        if not isinstance(other, User):
            return NotImplemented
        return self.id_user == other.id_user

    def __hash__(self) -> int:
        """
        Return a hash of the user.

        The hash is based on the identifier only, which keeps it consistent
        with ``__eq__``.

        Returns
        -------
        int
            Hash value of the user identifier.
        """
        return hash(self.id_user)
