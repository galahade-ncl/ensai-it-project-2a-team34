from pydantic import BaseModel, EmailStr, field_validator


class UserModel(BaseModel):
    """
    Data contract between the frontend and the backend for a user.

    Defines the JSON structure used to exchange user information,
    ensuring data consistency and validation during API requests and
    responses.

    Attributes
    ----------
    username : str
        Name of the user.
    password : str
        Password of the user (at least 16 characters).
    email : EmailStr
        Email of the user.
    """

    username: str
    password: str
    email: EmailStr
    # access_token: str

    @field_validator("password")
    @classmethod
    def check_password_length(cls, v: str) -> str:
        """
        Check that the password has good length (between 16 and 64 caracters).

        Parameters
        ----------
        v : str
            Password to validate.

        Returns
        -------
        str
            The password, unchanged.

        Raises
        ------
        ValueError
            If the password has fewer than 16 characters.
        ValueError
            If the password has more than 64 characters.
            We need to raise an error because bcrypt wouldn't work well.
        """
        min_len = 16
        if len(v) < min_len:
            raise ValueError(f"Password must be at least {min_len} characters long")
        if len(v) > 64:
            raise ValueError(f"Password must be at least {min_len} characters long")
        return v


# Autre que la création du user
class UserResponseModel(BaseModel):
    """
    Model used to update an existing user.

    Attributes
    ----------
    id_user : int
        Unique identifier of the user.
    username : str
        Name of the user.
    password : str
        Password of the user.
    email : EmailStr
        Email of the user.
    """

    id_user: int
    username: str
    password: str
    email: EmailStr
    # access_token: str


class UserReadModel(BaseModel):
    """
    Model returned when user information is read.

    Attributes
    ----------
    id_user : int
        Unique identifier of the user.
    username : str
        Name of the user.
    email : EmailStr
        Email of the user.
    access_token : str or None
        Access token of the user.
    """

    id_user: int
    username: str
    email: EmailStr
    access_token: str | None


class UserLoginModel(BaseModel):
    """
    Credentials sent to log in.

    Attributes
    ----------
    username : str
        Name of the user.
    password : str
        Password of the user.
    """

    username: str
    password: str
