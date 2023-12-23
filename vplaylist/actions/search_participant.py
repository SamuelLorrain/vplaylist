from typing import Optional

from vplaylist.app import app
from vplaylist.entities.video import Participant
from vplaylist.repositories.participant_repository import ParticipantRepository


def search_participant(search: Optional[str]) -> list[Participant]:
    participant_repository = app(ParticipantRepository)  # type: ignore
    if search is None:
        return participant_repository.get_all()
    return participant_repository.search(search)
