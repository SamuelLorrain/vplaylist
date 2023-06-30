-- add rootpath per account relation
-- depends: 20230628_01_L0YZQ-add-accounts

CREATE TABLE IF NOT EXISTS "account_rootpath" (
    "account_uuid" BLOB NOT NULL,
    "rootpath_id" INTEGER NOT NULL,
    FOREIGN KEY ("account_uuid") REFERENCES "data_account"("uuid"),
    FOREIGN KEY ("rootpath_id") REFERENCES "data_rootpath"("id"),
    PRIMARY KEY("account_uuid", "rootpath_id")
);
