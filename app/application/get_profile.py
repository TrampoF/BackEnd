from uuid import UUID
from pydantic import BaseModel, computed_field
from app.repository.i_profile_repository import IProfileRepository


class Output(BaseModel):
    """
    Data transfer object for profile output.
    """

    id: UUID
    first_name: str
    last_name: str
    email: str

    @computed_field
    @property
    def full_name(self) -> str:
        """
        Returns the full name of the user.
        """
        return f"{self.first_name} {self.last_name}"


class GetProfile:
    """
    Entity to handle the retrieval of one profile by its id.
    """

    _profile_repository: IProfileRepository

    def __init__(self, profile_repository: IProfileRepository):
        self._profile_repository = profile_repository

    def execute(self, profile_id: UUID) -> None | Output:
        """
        Retrieves an users from the user
        repository using its id and converts them to Output objects.
        """
        profile = self._profile_repository.get_by_id(profile_id=profile_id)
        if profile is None:
            return None
        return Output(**profile.__dict__)
