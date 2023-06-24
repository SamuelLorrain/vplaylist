-- Add participant
-- depends: 20230622_02_l48TP-add-analytics


CREATE TABLE IF NOT EXISTS "data_participant" (
    "uuid" BLOB NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL UNIQUE,
    "note" integer NULL
);

CREATE TABLE IF NOT EXISTS "data_video_participant" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "video_uuid" BLOB NOT NULL REFERENCES "data_video" ("uuid") DEFERRABLE INITIALLY DEFERRED,
    "participant_uuid" bigint NOT NULL REFERENCES "data_participant" ("uuid") DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS "data_participant_type" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "participant_uuid" BLOB NOT NULL REFERENCES "data_participant" ("uuid") DEFERRABLE INITIALLY DEFERRED,
    "type_id" bigint NOT NULL REFERENCES "data_type" ("id") DEFERRABLE INITIALLY DEFERRED
);
