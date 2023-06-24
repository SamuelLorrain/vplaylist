from typing import Optional

from vplaylist.entities.video import Participant
from vplaylist.repositories.participant_repository import ParticipantRepository


def search_participant(search: Optional[str]) -> list[Participant]:
    participant_repository = ParticipantRepository()
    if search is None:
        return participant_repository.get_all()
    return participant_repository.search(search)
