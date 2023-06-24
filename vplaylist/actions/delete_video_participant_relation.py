from uuid import UUID

from vplaylist.repositories.participant_repository import ParticipantRepository


def delete_video_participant_relation(video_uuid: UUID, participant_uuid: UUID) -> bool:
    participant_repository = ParticipantRepository()
    participant_repository.delete_video_participant_relation(
        video_uuid, participant_uuid
    )
    return True
