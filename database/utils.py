from setting import *
import psycopg2


def get_db_connection():
    conn = psycopg2.connect(dbname='ping', user='limprog',
                            password=DB_PASSWORD, host='localhost')
    cur = conn.cursor()
    return conn, cur


def add_members(group_id, users, conn, cur) -> None:
    for user in users:
        cur.execute("""INSERT INTO "user" (tg_id, username, name, group_id) VALUES (%s, %s, %s, %s)""",
                    (user.id, user.username, user.first_name + " " + user.last_name, group_id))

    conn.commit()


