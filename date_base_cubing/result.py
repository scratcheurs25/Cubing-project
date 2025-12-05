from typing import List, Dict

from date_base_cubing.database import get_connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS result (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time INT NOT NULL,
            id_event_group INTEGER NOT NULL,
            user TEXT NOT NULL)""")
    conn.commit()
    conn.close()
init_db()

def get_result(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM groupe_event WHERE id = ?""", (id,))

    rows = cur.fetchall()

    conn.close()

    # rows est une liste de Row, on la convertit en liste de dict
    return [dict(r) for r in rows]
def add_result( id_event , id_group ):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO groupe_event (id_event ,id_group) VALUES (?, ?);""",
                (id_event, id_group))

    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return {"id": new_id, "id_user": id_event, "id_group": id_group}
def del_result(id):
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
def get_all_result():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""select * from groupe_event;""")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
