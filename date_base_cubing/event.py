from typing import List, Dict

from date_base_cubing.database import get_connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            icon TEXT NOT NULL,
            makerid INTEGER NOT NULL,
            rule TEXT NOT NULL)""")
    conn.commit()
    conn.close()
init_db()

def get_all_events() -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events")
    rows = cur.fetchall()
    conn.close()

    return [dict(r) for r in rows]

def add_event(name, icon , makerID , rule):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO events (name , icon , makerid ,rule) VALUES (?, ? ,? ,?)", (name, icon , makerID , rule))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"id": new_id, "name" : name , "icon": icon , "makerID": makerID , "rule": rule}

def get_event_by_id(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM events WHERE id = ?", (id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_event_by_name(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events WHERE name = ?", (name,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def del_events(id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM events WHERE id = ?;", (id,))

        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return True
    except:
        return False

def edit_events(id,name: str, icon :str , rule:str) -> Dict:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE events SET name = ? , icon = ? , rule = ? WHERE id = ?;",(name , icon, rule , id))
    conn.commit()
    conn.close()
    return {"id": id, "name": name, "icon" : icon , "rule": rule}

print(get_all_events())
print(get_event_by_id(1))
print(get_event_by_name("3x3"))