-- Add analytics
-- depends: 20230622_01_Pph6a-create-sql

CREATE TABLE IF NOT EXISTS  "video_analytics" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "timestamp" integer NOT NULL,
    "video_uuid" BLOB NOT NULL REFERENCES "data_video" ("uuid")
);

CREATE TABLE IF NOT EXISTS "analytic_event" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "type" text NOT NULL,
    "value" real NOT NULL,
    "timestamp" integer NOT NULL,
    "video_analytics_id" integer NOT NULL REFERENCES "video_analytics" ("id")
);
