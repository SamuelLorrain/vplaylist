from typing import Optional

from vplaylist.app import app
from vplaylist.entities.video import Tag
from vplaylist.repositories.tag_repository import TagRepository


def search_tag(search: Optional[str]) -> list[Tag]:
    tag_repository = app(TagRepository)  # type: ignore
    if search is None:
        return tag_repository.get_all()
    return tag_repository.search(search)
