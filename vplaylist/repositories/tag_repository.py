import sqlite3
from uuid import UUID, uuid4

from vplaylist.config.config_registry import ConfigRegistry
from vplaylist.entities.video import Tag


class TagRepository:
    def __init__(self) -> None:
        self.config_registry = ConfigRegistry()
        self.db_file = self.config_registry.db_file

    def get_all(self) -> list[Tag]:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        get_tag_query = """SELECT uuid, name, note FROM data_type"""
        cursor.execute(get_tag_query)
        tags = [
            Tag(uuid=i[0], name=i[1], note=i[2], tags=[])
            for i in cursor.fetchall()
        ]
        conn.close()
        return tags

    def search(self, search: str) -> list[Tag]:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        search_tag_query = """
            SELECT uuid, name, note
            FROM data_type
            WHERE lower(name) LIKE ?;
        """
        cursor.execute(search_tag_query, ("%" + search.lower() + "%",))
        tags = [
            Tag(uuid=i[0], name=i[1], note=i[2])
            for i in cursor.fetchall()
        ]
        conn.close()
        return tags

    def add_tag(self, name: str) -> Tag:
        conn = sqlite3.connect(self.db_file)
        uuid = uuid4()
        insert_tag_query = """
            INSERT INTO data_type(uuid, name)
            VALUES (?,?)
        """
        get_tag_query = """
            SELECT uuid, name, note
            FROM data_type
            WHERE uuid = ?;
        """
        conn.execute(insert_tag_query, (str(uuid), name))
        conn.commit()
        cursor = conn.cursor()
        cursor.execute(get_tag_query, (str(uuid),))
        query_result = cursor.fetchone()
        conn.close()
        return Tag(
            uuid=query_result[0], name=query_result[1], note=query_result[2]
        )

    def add_video_tag_relation(
        self, video_uuid: UUID, tag_uuid: UUID
    ) -> bool:
        conn = sqlite3.connect(self.db_file)
        insert_video_tag_query = """
            INSERT INTO data_video_type(video_uuid, type_uuid)
            VALUES (?,?)
        """
        conn.execute(
            insert_video_tag_query, (str(video_uuid), str(tag_uuid))
        )
        conn.commit()
        conn.close()
        return True

    def delete_video_tag_relation(
        self, video_uuid: UUID, tag_uuid: UUID
    ) -> bool:
        conn = sqlite3.connect(self.db_file)
        insert_video_tag_query = """
            DELETE FROM data_video_type
            WHERE video_uuid = ? AND type_uuid = ?
        """
        conn.execute(
            insert_video_tag_query, (str(video_uuid), str(tag_uuid))
        )
        conn.commit()
        conn.close()
        return True
