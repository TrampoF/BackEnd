
from pydantic import BaseModel

from app.services.i_auth_service import IAuthService


class Input(BaseModel):
    email: str
    password: str

class Output(BaseModel):
    access_token: str
    refresh_token: str
    email: str

class SignIn:
    def __init__(self, auth_service: IAuthService):
        self.auth_service = auth_service

    def execute(self, user_data: Input) -> Output:
        return self.auth_service.sign_in(user_data)