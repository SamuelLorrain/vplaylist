from typing import Optional

from vplaylist.entities.video import Tag
from vplaylist.repositories.tag_repository import TagRepository


def search_tag(search: Optional[str]) -> list[Tag]:
    tag_repository = TagRepository()
    if search is None:
        return tag_repository.get_all()
    return tag_repository.search(search)
