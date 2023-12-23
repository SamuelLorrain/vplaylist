from vplaylist.app import app
from vplaylist.entities.video import Participant
from vplaylist.repositories.participant_repository import ParticipantRepository


def create_participant(name: str) -> Participant:
    participant_repository = app(ParticipantRepository)  # type: ignore
    name = name.strip()
    return participant_repository.add_participant(name)
