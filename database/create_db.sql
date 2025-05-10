CREATE TABLE if not exists "group" (
    tg_id bigint PRIMARY KEY,
    name VARCHAR(128)
);

CREATE TABLE "user"(
    id SERIAL PRIMARY KEY,
    tg_id int,
    username VARCHAR(128),
    name VARCHAR(128),
    group_id bigint,
    FOREIGN KEY (group_id) REFERENCES "group" (tg_id)
);

CREATE TABLE "role" (
    id SERIAL PRIMARY KEY,
    group_id bigint,
    name VARCHAR(128),
    FOREIGN KEY (group_id) REFERENCES "group"(tg_id)
);

CREATE TABLE "user_role" (
    id SERIAL PRIMARY KEY,
    role_id int,
    user_id int,
    group_id bigint,
    FOREIGN KEY (group_id) REFERENCES "group" (tg_id),
    FOREIGN KEY (role_id) REFERENCES "role" (id)
);

COMMIT