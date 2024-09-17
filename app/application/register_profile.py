import uuid
from pydantic import (
    BaseModel,
    Field,
    ValidationInfo,
    field_validator,
    validate_email,
)
from pydantic_core import PydanticCustomError

from app.exceptions.email_already_taken_exception import EmailAlreadyTakenException
from app.exceptions.invalid_email_format_exception import InvalidEmailFormatException
from app.exceptions.password_confirmation_dot_not_match_exception import (
    PasswordConfirmationDotNotMatchException,
)
from app.repository.i_profile_repository import IProfileRepository


class Input(BaseModel):
    """
    Data transfer object for profile registration.
    """

    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
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


class RegisterProfile:
    """
    Entity to handle the registration of a new profile.
    """

    _profile_repository: IProfileRepository

    def __init__(self, profile_repository: IProfileRepository):
        self._profile_repository = profile_repository

    def execute(self, data: Input) -> uuid.UUID:
        """
        Executes the profile registration process.
        """
        Input.model_validate(data)
        existing_profile = self._profile_repository.get_by_email(data["email"])
        if existing_profile:
            raise EmailAlreadyTakenException()
        profile = self._profile_repository.register(data)
        print(profile)
        return uuid.UUID(profile.id)
