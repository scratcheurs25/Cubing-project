from typing import List, Dict

from date_base_cubing.database import get_connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS result (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time INT NOT NULL,
            id_event INTEGER NOT NULL,
            user_id TEXT NOT NULL)""")
    conn.commit()
    conn.close()
init_db()

def get_result(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM result WHERE id = ?""", (id,))

    rows = cur.fetchall()

    conn.close()

    # rows est une liste de Row, on la convertit en liste de dict
    return [dict(r) for r in rows]
def add_result( time , id_event , user ):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO result (time , id_event ,user_id) VALUES (?, ? ,?);""",
                (time , id_event, user))

    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return {"id": new_id, "time": time, "id_event": id_event , "user_id" : user}
def del_result(id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM result WHERE id = ?;", (id,))

        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return True
    except:
        return False
def get_all_result():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""select * from result;""")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
def get_all_result_from_user_in_event(event_id,user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""   Select * from result where user_id = ? and id_event = ?  """, (user_id , event_id))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
