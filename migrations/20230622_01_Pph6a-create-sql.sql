-- create sql
-- depends:

CREATE TABLE IF NOT EXISTS "data_rootpath" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "path" text NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS "data_studio" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(100) NOT NULL UNIQUE,
    "note" integer NULL
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
