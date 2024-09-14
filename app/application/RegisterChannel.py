from typing import List
from pydantic import BaseModel
from app.repository.IChannelRepository import IChannelRepository


class RegisterChannelInput(BaseModel):
    chat_identifier: str
    api_key: str
    channel_name: str
    tags: List[str]


class RegisterChannelOutput(BaseModel):
    channel_id: int


class RegisterChannel:
    def __init__(self, channel_repository: IChannelRepository):
        self._channel_repository = channel_repository

    def run(self, register_input: RegisterChannelInput) -> RegisterChannelOutput:
        channel = self._channel_repository.create_channel(register_input)
        return RegisterChannelOutput(**channel)
