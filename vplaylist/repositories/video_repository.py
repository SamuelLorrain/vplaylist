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
                   lu
            from data_video
            join data_rootpath on data_video.rootpath_id = data_rootpath.id
            where uuid = ?
        """,
            (str(uuid),),
        )
        result = cursor.fetchone()
        return Video(
            path=Path(result[0]),
            rootpath=RootPath(path=Path(result[1])),
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
                "data_video_type", "data_video_type.video_id = data_video.id"
            )
            .add_outer_join("data_type", "data_video_type.type_id = data_type.id")
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
                    "data_video.name",
                    "data_type.name",
                    "data_type.note",
                    "data_video.path",
                ]
            )
        )
        params = data_video_query.get_params()
        query_string = data_video_query.get_query_string()
        db_connection = sqlite3.connect(str(self.db_file))
        results = db_connection.execute(query_string, params).fetchall()
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
            tags=[Tag(name=i[9], note=i[10]) for i in results if i[9] is not None],
            date_down=datetime.strptime(video_detail_except_tags[2], "%Y-%m-%d").date(),
            lu=video_detail_except_tags[4],
            height=video_detail_except_tags[5],
            width=video_detail_except_tags[6],
            note=video_detail_except_tags[7],
            name=video_detail_except_tags[8],
            path=video_detail_except_tags[9],
        )
        return video_details

    def _fetch_participants_details_from_video(self, uuid: UUID) -> list[Participant]:
        data_participants_query = (
            QueryConstructor("data_participant")
            .add_where_clause("data_video.uuid = ?")
            .add_outer_join(
                "data_participant_type",
                "data_participant_type.participant_id = data_participant.id",
            )
            .add_outer_join("data_type", "data_participant_type.type_id = data_type.id")
            .add_join(
                "data_video_participant",
                "data_video_participant.participant_id = data_participant.id",
            )
            .add_join("data_video", "data_video_participant.video_id = data_video.id")
            .add_param(str(uuid))
            .add_select(
                [
                    "data_participant.name",
                    "data_participant.note",
                    "data_type.name",
                    "data_type.note",
                ]
            )
        )
        params = data_participants_query.get_params()
        query_string = data_participants_query.get_query_string()
        db_connection = sqlite3.connect(str(self.db_file))
        results = db_connection.execute(query_string, params).fetchall()
        HashableParticipant = namedtuple("HashableParticipant", ["name", "note"])
        actor_mapping: MutableMapping[HashableParticipant, list[Tag]] = dict()
        for i in results:
            participant = HashableParticipant(name=i[0], note=i[1])
            tag = Tag(name=i[2], note=i[3])
            if actor_mapping.get(participant, False):
                actor_mapping[participant].append(tag)
            else:
                actor_mapping[participant] = [tag]
        participant_list: list[Participant] = []
        for key, value in actor_mapping.items():
            participant_list.append(
                Participant(name=key.name, note=key.note, tags=value)
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
