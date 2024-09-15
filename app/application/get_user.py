from uuid import UUID
from pydantic import BaseModel
from app.repository.iuser_repository import IUserRepository


class Output(BaseModel):
    """
    Data transfer object for user output.
    """

    id: UUID
    first_name: str
    last_name: str
    full_name: str
    email: str
    username: str


class GetUser:
    """
    Entity to handle the retrieval of one user by its id.
    """

    _user_repository: IUserRepository

    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    def execute(self, user_id: UUID) -> None | Output:
        """
        Retrieves an users from the user 
        repository using its id and converts them to Output objects.
        """
        user = self._user_repository.get_by_id(user_id=user_id)
        if user is None:
            return None
        user["full_name"] = f'{user["first_name"]} {user["last_name"]}'
        return Output(**user)
