from uuid import UUID

from vplaylist.repositories.tag_repository import TagRepository


def delete_video_tag_relation(video_uuid: UUID, tag_uuid: UUID) -> bool:
    tag_repository = TagRepository()
    tag_repository.delete_video_tag_relation(
        video_uuid, tag_uuid
    )
    return True
