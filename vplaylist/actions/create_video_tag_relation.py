from uuid import UUID

from vplaylist.repositories.tag_repository import TagRepository


def create_video_tag_relation(video_uuid: UUID, tag_uuid: UUID) -> bool:
    tag_repository = TagRepository()
    tag_repository.add_video_tag_relation(video_uuid, tag_uuid)
    return True
