from uuid import UUID
from pydantic import BaseModel
from app.repository.i_profile_repository import IProfileRepository


class Output(BaseModel):
    """
    Data transfer object for profile output.
    """

    id: UUID
    first_name: str
    last_name: str
    full_name: str
    email: str


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
        profile["full_name"] = f'{profile["first_name"]} {profile["last_name"]}'
        return Output(**profile)
