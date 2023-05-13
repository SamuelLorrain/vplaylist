import os
import sqlite3
from pathlib import Path
import json
import re
import subprocess
import datetime
from dataclasses import dataclass
from uuid import UUID
from vplaylist.config.config_registry import ConfigRegistry

@dataclass
class VideoPath:
    rootpath: Path
    path: Path

class DatabaseService:
    def __init__(self):
        self.config_registry = ConfigRegistry()
        self.db_file = self.config_registry.db_file
        self.db_paths = self.config_registry.db_paths
        self.ignore_paths = self.config_registry.ignore_paths

    def fetch_video_from_uuid(self, uuid: UUID) -> VideoPath:
        db_connection = sqlite3.connect(self.db_file)
        cursor = db_connection.execute("""
            select data_rootpath.path, data_video.path
            from data_video
            join data_rootpath on data_video.rootpath_id = data_rootpath.id
            where uuid = ?
        """, (str(uuid),))
        result = cursor.fetchone()
        return VideoPath(rootpath=Path(result[0]), path=Path(result[1]))

    def insert_new_elements_in_database(self):
        """Insert data to the database based on DB_PATHS config variable"""

        def get_key_from_list_of_dict(lst, key):
            for i in lst:
                if i.get(key):
                    return i.get(key)
            return None

        files = []
        # TODO put connection low level logic in another service
        dbConnection = sqlite3.connect(self.db_file)
        for path in self.db_paths:
            dbConnection.execute(
                "INSERT OR IGNORE INTO data_rootpath(path) VALUES (?)", (path,)
            )
            for dirpath, dirnames, filenames in os.walk(path):
                ignore = False
                if any([dirpath.startswith(i) for i in self.ignore_paths]):
                    print(f"ignoring {dirpath}!")
                    ignore = True
                if ignore:
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
                        files.append(
                            (
                                os.path.join(dirpath, filename).replace(path, ""),
                                path,
                                os.path.getmtime(os.path.join(dirpath, filename)),
                            )
                        )

        for filename, path, date in files:
            date = datetime.fromtimestamp(date).strftime("%Y-%m-%d")
            if (
                dbConnection.execute(
                    "SELECT id FROM data_video WHERE path = ?", (filename,)
                ).fetchone()
                is None
            ):
                print("insert {}".format(filename))
                ffProbe = subprocess.Popen(
                    [
                        "ffprobe",
                        "-v",
                        "error",
                        "-show_entries",
                        "stream=width,height",
                        "-of",
                        "json",
                        path + filename,
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
                    dbConnection.execute(
                        """
                        INSERT OR IGNORE INTO data_video(
                            rootpath_id,
                            path,
                            date_down,
                            height,
                            width
                        )
                        SELECT id,?,?,?,? FROM data_rootpath WHERE path = ?""",
                        (
                            filename,
                            date,
                            height,
                            width,
                            path,
                        ),
                    )
                else:
                    dbConnection.execute(
                        """
                        INSERT OR IGNORE INTO data_video(
                            rootpath_id,
                            path,
                            date_down,
                        )
                        SELECT id,?,? FROM rootpath WHERE path = ?""",
                        (
                            filename,
                            date,
                            path,
                        ),
                    )
        dbConnection.commit()
        dbConnection.close()
        return True

    def delete_non_existing_files_from_database(self):
        """Clean the database

        Check for all the video that doesn't exists
        in the filesystem and delete them from
        the sqlite3 database.
        """
        dbPath = self.db_file
        dbConnection = sqlite3.connect(str(dbPath))
        cleanQuery = """SELECT data_video.id,data_rootpath.path,data_video.path
                        FROM data_video JOIN data_rootpath ON
                        data_video.rootpath_id = data_rootpath.id"""
        for videorowid, rootpath, videopath in dbConnection.execute(cleanQuery):
            if not os.path.exists(rootpath + videopath):
                print("Video {} doesn't exists".format(rootpath + videopath))
                dbConnection.execute(
                    "DELETE FROM data_video WHERE id = ?", (videorowid,)
                )

        dbConnection.commit()
        dbConnection.close()
        return True
