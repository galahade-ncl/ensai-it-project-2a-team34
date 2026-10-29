from pydantic import BaseModel, EmailStr, field_validator


class UserModel(BaseModel):
    """Acts as the data contract between the frontend and the backend.

    It defines the JSON structure used to exchange user information,
    ensuring data consistency and validation during API requests and responses."""

    id_user: int | None = None
    username: str
    password: str
    email: EmailStr
    # access_token: str

    @field_validator("password")
    @classmethod
    def check_password_length(cls, v: str) -> str:
        min_len = 16
        if len(v) < min_len:
            raise ValueError(f"Password must be at least {min_len} characters long")
        return v


class UserReadModel(BaseModel):
    id_user: int
    username: str
    email: EmailStr
    access_token: str | None


class UserLoginModel(BaseModel):
    username: str
    password: str
