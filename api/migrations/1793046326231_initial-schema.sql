-- Up Migration
CREATE TABLE "plants" (
  "id" integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "name" varchar(255) UNIQUE NOT NULL,
  "image_path" varchar(1024),
  "created_at" timestamptz NOT NULL DEFAULT (now()),
  "deleted_at" timestamptz
);

CREATE TABLE "plant_tasks" (
  "id" integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "name" varchar(255) UNIQUE NOT NULL
);

CREATE TABLE "plant_task_schedules" (
  "id" integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "plant_id" integer NOT NULL,
  "task_id" integer NOT NULL,
  "frequency_days" integer NOT NULL CHECK (frequency_days > 0),
  "created_at" timestamptz NOT NULL DEFAULT (now()),
  "deleted_at" timestamptz,
  "started_at" timestamptz NOT NULL DEFAULT (now()),
  "stopped_at" timestamptz
);

CREATE TABLE "plant_task_completion_history" (
  "id" integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "plant_id" integer NOT NULL,
  "task_id" integer NOT NULL,
  "completed_at" timestamptz NOT NULL DEFAULT (now()),
  "data" jsonb
);

CREATE UNIQUE INDEX "idx_plant_task_schedules_plant_id_task_d" ON "plant_task_schedules" ("plant_id", "task_id");

CREATE INDEX "idx_plant_history_task_time" ON "plant_task_completion_history" ("plant_id", "task_id", "completed_at");

ALTER TABLE "plant_task_schedules" ADD FOREIGN KEY ("plant_id") REFERENCES "plants" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "plant_task_schedules" ADD FOREIGN KEY ("task_id") REFERENCES "plant_tasks" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "plant_task_completion_history" ADD FOREIGN KEY ("plant_id") REFERENCES "plants" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "plant_task_completion_history" ADD FOREIGN KEY ("task_id") REFERENCES "plant_tasks" ("id") DEFERRABLE INITIALLY IMMEDIATE;

-- Down Migration

DROP TABLE plant_task_completion_history;
DROP TABLE plant_task_schedules;
DROP TABLE plant_tasks;
DROP TABLE plants;