from typing import List, Dict

from date_base_cubing.database import get_connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS groupe_user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            id_group INTEGER NOT NULL)""")
    conn.commit()
    conn.close()
init_db()

def get_group_user(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM groupe_user WHERE id = ?""", (id,))

    rows = cur.fetchall()

    conn.close()

    # rows est une liste de Row, on la convertit en liste de dict
    return [dict(r) for r in rows]
def add_group_user( id_user , id_group ):
    print(id_user)
    print(id_group)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO groupe_user (id_user ,id_group) VALUES (?, ?);""",
                (id_user, id_group))

    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return {"id": new_id, "id_user": id_user, "id_group": id_group}
def del_group_user(id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM groupe_user WHERE id = ?;", (id,))

        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return True
    except:
        return False
def get_all_groups_user():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""select * from groupe_user;""")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_users_from_group(group_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""Select * from users inner join groupe_user on groupe_user.id_user = users.id where groupe_user.id_group = ?;""", (group_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
def del_user_from_group(user_id , group_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""DELETE FROM groupe_user WHERE id_user = ? AND id_group = ?;""", (user_id,group_id))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return [dict(r) for r in rows]
