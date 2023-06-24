from vplaylist.entities.video import Tag
from vplaylist.repositories.tag_repository import TagRepository


def create_tag(name: str) -> Tag:
    tag_repository = TagRepository()
    name = name.strip()
    return tag_repository.add_tag(name)
