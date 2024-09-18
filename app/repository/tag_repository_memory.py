import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, create_model
from app.models.tag import Tag
from app.repository.i_tag_repository import ITagRepository
from app.schemas.create_tag_schema import CreateTagSchema


class TagRepositoryMemory(ITagRepository):

    _tags = List[Tag]

    def __init__(self):
        self._tags = []

    def get_tags(self) -> List[Tag]:
        return self._tags

    def get_tags_by_profile_id(self, profile_id: UUID) -> List[Tag]:
        return [tag for tag in self._tags if tag.profile_id == profile_id]

    def create_tag(self, tag_data: CreateTagSchema) -> Tag:
        tag_data = CreateTagSchema(
            **tag_data.model_dump(),
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        self._tags.append(tag_data)
        return Tag(**tag_data.model_dump())

    def create_tags(self, tags: List[str], profile_id: UUID) -> List[Tag]:
        created_tags = []
        for tag in tags:
            tag_data = CreateTagSchema(
                name=tag,
                profile_id=profile_id,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            )
            self._tags.append(tag_data)
            created_tags.append(tag_data)
        return created_tags
