import uuid
from pydantic import (
    BaseModel,
    Field,
    ValidationInfo,
    field_validator,
    validate_email,
)
from pydantic_core import PydanticCustomError
from app.exceptions.invalid_email_format_exception import InvalidEmailFormatException
from app.exceptions.password_confirmation_dot_not_match_exception import (
    PasswordConfirmationDotNotMatchException,
)
from app.repository.iuser_repository import IUserRepository


class Input(BaseModel):
    """
    Data transfer object for user registration.
    """

    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8)
    password_confirmation: str = Field(...)

    @field_validator("password_confirmation")
    @classmethod
    def check_password_password_confirmation_match(
        cls, password_confirmation_value: str, info: ValidationInfo
    ) -> str:
        """
        Validates that the password confirmation matches the original password.
        """
        if (
            "password" in info.data
            and password_confirmation_value != info.data["password"]
        ):
            raise PasswordConfirmationDotNotMatchException()
        return password_confirmation_value

    @field_validator("email")
    @classmethod
    def check_email_formatr(cls, email_value: str) -> str:
        """
        Validates that the email is in the correct format.
        """
        try:
            validate_email(email_value)
            return email_value
        except PydanticCustomError as e:
            raise InvalidEmailFormatException() from e


class RegisterUser:
    """
    Entity to handle the registration of a new user.
    """

    _user_repository: IUserRepository

    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    def execute(self, data: Input) -> uuid.UUID:
        """
        Executes the user registration process.
        """

        Input.model_validate(data)
        user_id = uuid.uuid4()
        data["id"] = user_id
        self._user_repository.create_user(user=data)
        return user_id
