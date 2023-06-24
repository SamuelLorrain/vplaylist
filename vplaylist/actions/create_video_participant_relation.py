from uuid import UUID

from vplaylist.repositories.participant_repository import ParticipantRepository


def create_video_participant_relation(video_uuid: UUID, participant_uuid: UUID) -> bool:
    participant_repository = ParticipantRepository()
    participant_repository.add_video_participant_relation(video_uuid, participant_uuid)
    return True
