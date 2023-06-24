-- add types_tags
-- depends: 20230624_01_fLmeD-add-participant


CREATE TABLE IF NOT EXISTS "data_type" (
    "uuid" blob NOT NULL PRIMARY KEY,
    "name" varchar(30) NOT NULL UNIQUE,
    "note" integer NULL
);

CREATE TABLE IF NOT EXISTS "data_video_type" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "video_uuid" blob NOT NULL REFERENCES "data_video" ("uuid") DEFERRABLE INITIALLY DEFERRED,
    "type_uuid" blob NOT NULL REFERENCES "data_type" ("uuid") DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS "data_participant_type" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "participant_uuid" BLOB NOT NULL REFERENCES "data_participant" ("uuid") DEFERRABLE INITIALLY DEFERRED,
    "type_uuid" bigint NOT NULL REFERENCES "data_type" ("uuid") DEFERRABLE INITIALLY DEFERRED
);
