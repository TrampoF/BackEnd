import datetime
from pydantic import BaseModel, ConfigDict


class RegisterProfileSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    first_name: str
    last_name: str
    email: str
    password: str
