from vplaylist.app import app
from vplaylist.entities.video import Tag
from vplaylist.repositories.tag_repository import TagRepository


def create_tag(name: str) -> Tag:
    tag_repository = app(TagRepository)  # type: ignore
    name = name.strip()
    return tag_repository.add_tag(name)
