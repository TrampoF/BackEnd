import datetime
import uuid
from typing import List
from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.repository.i_tag_repository import ITagRepository


class TagRepositoryDatabase(ITagRepository):
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def get_tags(self) -> List[Tag]:
        return self._session.query(Tag).all()

    def get_tags_by_profile_id(self, profile_id) -> List[Tag]:
        return self._session.query(Tag).filter(Tag.profile_id == profile_id).all()

    def create_tag(self, tag_data) -> Tag:
        tag = Tag(**tag_data.model_dump(), created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
        print(tag)
        self._session.add(tag)
        return tag

    def create_tags(self, tags: List[str], profile_id: uuid.UUID) -> List[Tag]:
        created_tags = []
        for tag in tags:
            tag_data = Tag(name=tag, profile_id=profile_id, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
            self._session.add(tag_data)
            created_tags.append(tag_data)
        self._session.commit()
        return created_tags
