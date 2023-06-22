-- create sql
-- depends:

CREATE TABLE IF NOT EXISTS "data_rootpath" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "path" text NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS "data_studio_type" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "studio_id" bigint NOT NULL REFERENCES "data_studio" ("id") DEFERRABLE INITIALLY DEFERRED,
    "type_id" bigint NOT NULL REFERENCES "data_type" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS "data_participant_type" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "participant_id" bigint NOT NULL REFERENCES "data_participant" ("id") DEFERRABLE INITIALLY DEFERRED,
    "type_id" bigint NOT NULL REFERENCES "data_type" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS "data_participant" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(100) NOT NULL UNIQUE,
    "note" integer NULL
);

CREATE TABLE IF NOT EXISTS "data_studio" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(100) NOT NULL UNIQUE,
    "note" integer NULL
);

CREATE TABLE IF NOT EXISTS "data_type" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(30) NOT NULL UNIQUE,
    "note" integer NULL
);

CREATE TABLE IF NOT EXISTS "data_video_participant" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "video_id" bigint NOT NULL REFERENCES "data_video" ("id") DEFERRABLE INITIALLY DEFERRED,
    "participant_id" bigint NOT NULL REFERENCES "data_participant" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS "data_video_type" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "video_id" bigint NOT NULL REFERENCES "data_video" ("id") DEFERRABLE INITIALLY DEFERRED,
    "type_id" bigint NOT NULL REFERENCES "data_type" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS "data_video" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "path" text NOT NULL UNIQUE,
    "film" varchar(500) NULL,
    "date_down" date NULL,
    "note" integer NULL,
    "lu" bool NULL,
    "height" integer NOT NULL,
    "width" integer NOT NULL,
    "rootpath_id" bigint NOT NULL REFERENCES "data_rootpath" ("id") DEFERRABLE INITIALLY DEFERRED,
    "studio_id" bigint NULL REFERENCES "data_studio" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(500) NULL,
    "uuid" BLOB
);

CREATE TABLE IF NOT EXISTS "data_best_search"(
    "search_term" TEXT NOT NULL
);
