from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CreateChannelSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    profile_id: UUID
    chat_identifier: str
    channel_name: str
    tags: list[str]