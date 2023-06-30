import json
import os
import re
import sqlite3
import subprocess
from collections import namedtuple
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import MutableMapping, Optional
from uuid import UUID, uuid4

from vplaylist.config.config_registry import ConfigRegistry
from vplaylist.entities.playlist import RootPath, Video
from vplaylist.entities.video import Film, Participant, Tag, VideoDetails
from vplaylist.utils.query_constructor import QueryConstructor


@dataclass
class VideoPathFromFileSystem:
    rootpath: Path
    fullpath: Path
    dirpath: Path
    filename_without_rootpath: Path
    timestamp: float


class VideoRepository:
    def __init__(self) -> None:
        self.config_registry = ConfigRegistry()
        self.db_file = self.config_registry.db_file
        self.db_paths = self.config_registry.db_paths
        self.ignore_paths = self.config_registry.ignore_paths

    def get_all_generator(self):
        db_connection = sqlite3.connect(self.db_file)
        query = """
            select data_video.path,
                   data_rootpath.path,
                   height,
                   width,
                   uuid,
                   name,
                   film,
                   date_down,
                   note,
                   lu,
                   data_rootpath.id as 'data_rootpath_id'
            from data_video
            join data_rootpath on data_video.rootpath_id = data_rootpath.id
        """
        result = db_connection.execute(query)
        d: list[tuple] = list(tuple())

        def video_from_result(video_result: tuple) -> Video:
            return Video(
                path=Path(video_result[0]),
                rootpath=RootPath(
                    id=video_result[10],
                    path=Path(video_result[1])
                ),
                height=video_result[2],
                width=video_result[3],
                uuid=video_result[4],
                name=video_result[5],
                film=video_result[6],
                date_down=video_result[7],
                note=video_result[8],
                lu=video_result[9],
            )
        while d is not None:
            d = result.fetchone()
            if d is None:
                break
            yield video_from_result(d)
        db_connection.close()


    def fetch_video(self, uuid: UUID) -> Video:
        db_connection = sqlite3.connect(self.db_file)
        cursor = db_connection.execute(
            """
            select data_video.path,
                   data_rootpath.path,
                   height,
                   width,
                   uuid,
                   name,
                   film,
                   date_down,
                   note,
                   lu,
                   data_rootpath.id as data_rootpath_id
            from data_video
            join data_rootpath on data_video.rootpath_id = data_rootpath.id
            where uuid = ?
        """,
            (str(uuid),),
        )
        result = cursor.fetchone()
        return Video(
            path=Path(result[0]),
            rootpath=RootPath(id=result[10], path=Path(result[1])),
            height=result[2],
            width=result[3],
            uuid=result[4],
            name=result[5],
            film=result[6],
            date_down=result[7],
            note=result[8],
            lu=result[9],
        )

    def insert_new_videos(self) -> bool:
        new_videos_in_file_system = self._get_video_from_filesystem()
        return self._insert_new_elements_in_database(new_videos_in_file_system)

    def _insert_new_elements_in_database(
        self, files: list[VideoPathFromFileSystem]
    ) -> bool:
        """Insert data to the database based on DB_PATHS config variable"""

        def get_key_from_list_of_dict(
            lst: list[dict[str, str]], key: str
        ) -> str | None:
            for i in lst:
                if i.get(key):
                    return i.get(key)
            return None

        db_connection = sqlite3.connect(self.db_file)
        for file in files:
            formatted_date = date.fromtimestamp(file.timestamp).strftime("%Y-%m-%d")
            if (
                db_connection.execute(
                    "SELECT id FROM data_video WHERE path = ?",
                    (str(file.filename_without_rootpath),),
                ).fetchone()
                is None
            ):
                print("insert {}".format(file.filename_without_rootpath))
                print(formatted_date)
                print(str(file.rootpath))
                ffProbe = subprocess.Popen(
                    [
                        "ffprobe",
                        "-v",
                        "error",
                        "-show_entries",
                        "stream=width,height",
                        "-of",
                        "json",
                        str(file.fullpath),
                    ],
                    stdout=subprocess.PIPE,
                )
                ffProbeReturn = json.loads(ffProbe.communicate()[0])

                width = (
                    get_key_from_list_of_dict(ffProbeReturn["streams"], "width")
                    if ffProbeReturn.get("streams")
                    else None
                )
                height = (
                    get_key_from_list_of_dict(ffProbeReturn["streams"], "height")
                    if ffProbeReturn.get("streams")
                    else None
                )

                if width and height:
                    db_connection.execute(
                        """
                        INSERT INTO data_video(
                            rootpath_id,
                            path,
                            date_down,
                            height,
                            width,
                            uuid
                        )
                        SELECT id,?,?,?,?,? FROM data_rootpath WHERE path = ?""",
                        (
                            str(file.filename_without_rootpath),
                            formatted_date,
                            height,
                            width,
                            str(uuid4()),
                            str(file.rootpath) + "/",
                        ),
                    )
                else:
                    db_connection.execute(
                        """
                        INSERT INTO data_video(
                            rootpath_id,
                            path,
                            date_down,
                            uuid
                        )
                        SELECT id,?,?,? FROM data_rootpath WHERE path = ?""",
                        (
                            str(file.filename_without_rootpath),
                            formatted_date,
                            str(uuid4()),
                            str(file.rootpath) + "/",
                        ),
                    )
        db_connection.commit()
        db_connection.close()
        return True

    def _get_video_from_filesystem(self) -> list[VideoPathFromFileSystem]:
        files = []
        for rootpath in self.db_paths:
            for dirpath, _, filenames in os.walk(str(rootpath)):
                if any([dirpath.startswith(str(i)) for i in self.ignore_paths]):
                    print(f"ignoring {dirpath}!")
                    break
                for filename in filenames:
                    if (
                        re.match(
                            r".*\.(mp4|webm|avi|mkv|flv|wmv|mpg)",
                            filename,
                            re.IGNORECASE,
                        )
                        is not None
                    ):
                        fullpath = Path(os.path.join(dirpath, filename))
                        filename_without_rootpath = Path(
                            str(fullpath).replace(str(rootpath) + "/", "")
                        )
                        files.append(
                            VideoPathFromFileSystem(
                                fullpath=fullpath,
                                rootpath=Path(rootpath),
                                dirpath=Path(dirpath),
                                filename_without_rootpath=filename_without_rootpath,
                                timestamp=os.path.getmtime(
                                    os.path.join(dirpath, filename)
                                ),
                            )
                        )
        return files

    def fetch_video_details(self, uuid: UUID) -> Optional[VideoDetails]:
        data_video_query = (
            QueryConstructor("data_video")
            .add_where_clause("data_video.uuid = ?")
            .add_outer_join(
                "data_video_type", "data_video_type.video_uuid = data_video.uuid"
            )
            .add_outer_join("data_type", "data_video_type.type_uuid = data_type.uuid")
            .add_param(str(uuid))
            .add_select(
                [
                    "data_video.name",
                    "data_video.film",
                    "data_video.date_down",
                    "data_video.note",
                    "data_video.lu",
                    "data_video.height",
                    "data_video.width",
                    "data_video.note",
                    "data_type.name",
                    "data_type.note",
                    "data_video.path",
                    "data_type.uuid",
                ]
            )
        )
        params = data_video_query.get_params()
        query_string = data_video_query.get_query_string()
        db_connection = sqlite3.connect(str(self.db_file))
        results = db_connection.execute(query_string, params).fetchall()
        print(results)
        if len(results) < 1:
            return None
        video_detail_except_tags = results[0]
        db_connection.close()
        video_details = VideoDetails(
            uuid=uuid,
            participants=self._fetch_participants_details_from_video(uuid),
            film=Film(name=video_detail_except_tags[1])
            if video_detail_except_tags[1] is not None
            else None,
            studio=None,
            tags=[Tag(name=i[8], note=i[9], uuid=UUID(i[11])) for i in results if i[11] is not None],
            date_down=datetime.strptime(video_detail_except_tags[2], "%Y-%m-%d").date(),
            lu=video_detail_except_tags[4],
            height=video_detail_except_tags[5],
            width=video_detail_except_tags[6],
            note=video_detail_except_tags[3],
            name=video_detail_except_tags[0],
            path=video_detail_except_tags[10],
        )
        return video_details

    def _fetch_participants_details_from_video(self, uuid: UUID) -> list[Participant]:
        data_participants_query = (
            QueryConstructor("data_participant")
            .add_where_clause("data_video.uuid = ?")
            .add_outer_join(
                "data_participant_type",
                "data_participant_type.participant_uuid = data_participant.uuid",
            )
            .add_outer_join("data_type", "data_participant_type.type_uuid = data_type.uuid")
            .add_join(
                "data_video_participant",
                "data_video_participant.participant_uuid = data_participant.uuid",
            )
            .add_join(
                "data_video", "data_video_participant.video_uuid = data_video.uuid"
            )
            .add_param(str(uuid))
            .add_select(
                [
                    "data_participant.name",
                    "data_participant.note",
                    "data_type.name",
                    "data_type.note",
                    "data_participant.uuid as data_participant_uuid",
                    "data_type.uuid as data_type_uuid",
                ]
            )
        )
        params = data_participants_query.get_params()
        query_string = data_participants_query.get_query_string()
        db_connection = sqlite3.connect(str(self.db_file))
        results = db_connection.execute(query_string, params).fetchall()
        HashableParticipant = namedtuple(
            "HashableParticipant", ["name", "note", "uuid"]
        )
        actor_mapping: MutableMapping[HashableParticipant, list[Tag]] = dict()
        for i in results:
            participant = HashableParticipant(name=i[0], note=i[1], uuid=UUID(i[4]))
            if i[2]:
                tag = Tag(name=i[2], note=i[3], uuid=i[5])
                if actor_mapping.get(participant, False):
                    actor_mapping[participant].append(tag)
                else:
                    actor_mapping[participant] = [tag]
            else:
                actor_mapping[participant] = []
        participant_list: list[Participant] = []
        for key, value in actor_mapping.items():
            participant_list.append(
                Participant(name=key.name, note=key.note, tags=value, uuid=key.uuid)
            )

        return participant_list

    def clean_non_existent_videos(self) -> bool:
        db_connection = sqlite3.connect(str(self.db_file))
        clean_query = """SELECT data_video.id,data_rootpath.path,data_video.path
                        FROM data_video JOIN data_rootpath ON
                        data_video.rootpath_id = data_rootpath.id"""
        for video_rowid, rootpath, video_path in db_connection.execute(clean_query):
            if not os.path.exists(rootpath + video_path):
                print("Video {} doesn't exists".format(rootpath + video_path))
                db_connection.execute(
                    "DELETE FROM data_video WHERE id = ?", (video_rowid,)
                )
        db_connection.commit()
        db_connection.close()
        return True

    def modify_video(self, uuid: UUID, details: VideoDetails) -> bool:
        db_connection = sqlite3.connect(str(self.db_file))
        query_params = []
        sql_set_string = ""
        if details.name is not None:
            query_params.append(details.name)
            sql_set_string = sql_set_string + "\nSET name = ?"
        if details.note is not None:
            query_params.append(str(details.note))
            sql_set_string = sql_set_string + "\nSET note = ?"
        if details.date_down is not None:
            query_params.append(str(details.date_down))
            sql_set_string = sql_set_string + "\nSET date_down = ?"
        query_params.append(str(uuid))
        db_connection.execute(
            f"UPDATE data_video\n{sql_set_string}\nWHERE uuid = ?", query_params
        )
        db_connection.commit()
        db_connection.close()
        return True

    def video_is_in_rootpath(self, uuid: UUID, rootpaths: list[RootPath]) -> bool:
        db_connection = sqlite3.connect(str(self.db_file))
        query = (
            QueryConstructor("data_video")
            .add_select("uuid")
            .add_where_clause("uuid = ?")
            .add_where_clause(f"rootpath_id IN ({('?,'*len(rootpaths))[:-1]})")
        )
        query.add_param(str(uuid))
        for i in rootpaths:
            query.add_param(str(i.id))
        cursor = db_connection.execute(query.get_query_string(), query.get_params())
        result = cursor.fetchone()
        db_connection.close()
        if result:
            return True
        return False
