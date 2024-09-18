from typing import List
from uuid import UUID
from app.models.tag import Tag
from app.schemas.create_tag_schema import CreateTagSchema


class ITagRepository:
    """ """

    def get_tags(self) -> List[Tag]:
        """
        Retrieve all tags.
        """

    def get_tags_by_profile_id(self, profile_id: UUID) -> List[Tag]:
        """
        Retrieve all tags by profile ID.
        """

    def create_tag(self, tag_data: CreateTagSchema) -> Tag:
        """
        Create a new tag.
        """

    def create_tags(self, tags: List[str], profile_id: UUID) -> List[Tag]:
        """
        Create a list of tags.
        """
