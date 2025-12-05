from typing import List, Dict

from date_base_cubing.database import get_connection
from date_base_cubing import group_user
from date_base_cubing import group_event

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS groupe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            icon TEXT NOT NULL,
            makerid INTEGER NOT NULL)""")
    conn.commit()
    conn.close()
init_db()

def get_group(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM groupe WHERE id = ?""", (id,))

    rows = cur.fetchall()

    conn.close()

    # rows est une liste de Row, on la convertit en liste de dict
    return [dict(r) for r in rows]
def add_group( name, icon, makerid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO groupe (name , icon , makerid) VALUES (?, ?, ?);""",
                (name,icon,makerid))

    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return {"id": new_id, "name": name, "icon": icon, "makerid": makerid}
def del_group(id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM groupe WHERE id = ?;", (id,))

        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return True
    except:
        return False
def get_all_groups():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""select * from groupe;""")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_user_to_group(id_group, id_users):
    out = group_user.add_group_user(id_users , id_group)
    return out
def del_user_group(id):
    out = group_user.del_group_user(id)
def add_event_to_group(id_group, id_events):
    out = group_event.add_group_event(id_events , id_group)
    return out
def del_event_group(id):
    out = group_event.del_group_event(id)
    return out

def get_all_user_from_group(id_group):
    out = group_user.get_all_users_from_group(id_group)
    return out
def get_all_event_from_group(id_group):
    out = group_event.get_all_events_from_group(id_group)
    return out
def del_event_from_group(event_id , group_id):
    out = group_event.del_event_from_group(event_id, group_id)
    return out
def del_user_from_group(id_group, id_users):
    out = group_user.del_user_from_group(id_users,id_group)
    return out
def edit_group(id,name: str, icon : str , makerid: int) -> Dict:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE groupe SET name = ? , icon = ? , makerid = ? WHERE id = ?;",(name , icon , makerid, id))
    conn.commit()
    conn.close()
    return {"id": id, "name": name, "icon": icon, "makerid": makerid}
