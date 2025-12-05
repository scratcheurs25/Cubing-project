from typing import List, Dict

from date_base_cubing.database import get_connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS groupe_event (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_event INTEGER NOT NULL,
            id_group INTEGER NOT NULL)""")
    conn.commit()
    conn.close()
init_db()

def get_group_event(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM groupe_event WHERE id = ?""", (id,))

    rows = cur.fetchall()

    conn.close()

    # rows est une liste de Row, on la convertit en liste de dict
    return [dict(r) for r in rows]
def add_group_event( id_event , id_group ):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO groupe_event (id_event ,id_group) VALUES (?, ?);""",
                (id_event, id_group))

    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return {"id": new_id, "id_user": id_event, "id_group": id_group}
def del_group_event(id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM groupe_event WHERE id = ?;", (id,))

        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return True
    except:
        return False
def get_all_groups_event():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""select * from groupe_event;""")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_events_from_group(group_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""Select * from events inner join groupe_event on groupe_event.id_event = events.id where groupe_event.id_group = ?;""", (group_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def del_event_from_group(event_id , group_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""DELETE FROM groupe_user WHERE id_event = ? AND id_group = ?;""", (event_id,group_id))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return [dict(r) for r in rows]
