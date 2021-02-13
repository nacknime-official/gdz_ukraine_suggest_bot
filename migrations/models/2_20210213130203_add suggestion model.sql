-- upgrade --
CREATE TABLE IF NOT EXISTS "suggestions" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "is_approved" BOOL NOT NULL  DEFAULT False,
    "is_warned" BOOL NOT NULL  DEFAULT False,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "suggestions"."id" IS 'uses message id from moder channel';
-- downgrade --
DROP TABLE IF EXISTS "suggestions";
