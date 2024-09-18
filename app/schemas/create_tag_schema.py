from uuid import UUID
import datetime
from pydantic import BaseModel, ConfigDict


class CreateTagSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    profile_id: UUID
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
