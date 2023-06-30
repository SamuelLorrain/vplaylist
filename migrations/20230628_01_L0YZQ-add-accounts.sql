-- add accounts
-- depends: 20230624_02_XtTMl-add-types-tags

CREATE TABLE IF NOT EXISTS "data_account" (
    "uuid" BLOB NOT NULL PRIMARY KEY,
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "password" TEXT NOT NULL
);
