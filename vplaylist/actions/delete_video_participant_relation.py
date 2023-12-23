from uuid import UUID

from vplaylist.app import app
from vplaylist.repositories.participant_repository import ParticipantRepository


def delete_video_participant_relation(video_uuid: UUID, participant_uuid: UUID) -> bool:
    participant_repository = app(ParticipantRepository)  # type: ignore
    participant_repository.delete_video_participant_relation(
        video_uuid, participant_uuid
    )
    return True
