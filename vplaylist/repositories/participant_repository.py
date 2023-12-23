import sqlite3
from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from vplaylist.config.config_registry import ConfigRegistry
from vplaylist.entities.video import Participant


class ParticipantRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Participant]:
        raise NotImplementedError

    @abstractmethod
    def search(self, search: str) -> list[Participant]:
        raise NotImplementedError

    @abstractmethod
    def add_participant(self, name: str) -> Participant:
        raise NotImplementedError

    @abstractmethod
    def add_video_participant_relation(
        self, video_uuid: UUID, participant_uuid: UUID
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete_video_participant_relation(
        self, video_uuid: UUID, participant_uuid: UUID
    ) -> bool:
        raise NotImplementedError


class SqliteParticipantRepository(ParticipantRepository):
    def __init__(self) -> None:
        self.config_registry = ConfigRegistry()
        self.db_file = self.config_registry.db_file

    def get_all(self) -> list[Participant]:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        get_participant_query = """SELECT uuid, name, note FROM data_participant"""
        cursor.execute(get_participant_query)
        participants = [
            Participant(uuid=i[0], name=i[1], note=i[2], tags=[])
            for i in cursor.fetchall()
        ]
        conn.close()
        return participants

    def search(self, search: str) -> list[Participant]:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        search_participant_query = """
            SELECT uuid, name, note
            FROM data_participant
            WHERE lower(name) LIKE ?;
        """
        cursor.execute(search_participant_query, ("%" + search.lower() + "%",))
        participants = [
            Participant(uuid=i[0], name=i[1], note=i[2], tags=[])
            for i in cursor.fetchall()
        ]
        conn.close()
        return participants

    def add_participant(self, name: str) -> Participant:
        conn = sqlite3.connect(self.db_file)
        uuid = uuid4()
        insert_participant_query = """
            INSERT INTO data_participant(uuid, name)
            VALUES (?,?)
        """
        get_participant_query = """
            SELECT uuid, name, note
            FROM data_participant
            WHERE uuid = ?;
        """
        conn.execute(insert_participant_query, (str(uuid), name))
        conn.commit()
        cursor = conn.cursor()
        cursor.execute(get_participant_query, (str(uuid),))
        query_result = cursor.fetchone()
        conn.close()
        return Participant(
            uuid=query_result[0], name=query_result[1], note=query_result[2], tags=[]
        )

    def add_video_participant_relation(
        self, video_uuid: UUID, participant_uuid: UUID
    ) -> bool:
        conn = sqlite3.connect(self.db_file)
        insert_video_participant_query = """
            INSERT INTO data_video_participant(video_uuid, participant_uuid)
            VALUES (?,?)
        """
        conn.execute(
            insert_video_participant_query, (str(video_uuid), str(participant_uuid))
        )
        conn.commit()
        conn.close()
        return True

    def delete_video_participant_relation(
        self, video_uuid: UUID, participant_uuid: UUID
    ) -> bool:
        conn = sqlite3.connect(self.db_file)
        insert_video_participant_query = """
            DELETE FROM data_video_participant
            WHERE video_uuid = ? AND participant_uuid = ?
        """
        conn.execute(
            insert_video_participant_query, (str(video_uuid), str(participant_uuid))
        )
        conn.commit()
        conn.close()
        return True
