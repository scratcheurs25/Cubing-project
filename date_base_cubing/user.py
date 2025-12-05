import os
from typing import List, Dict
import hashlib

from date_base_cubing.database import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            wca STRING NULL , 
            password TEXT NOT NULL, 
            role BOOLEAN NOT NULL,
            icon TEXT NOT NULL)""")
    conn.commit()
    conn.close()
init_db()

def get_all_users() -> List[Dict]:
    """Retourne la liste de tous les élèves."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()

    conn.close()

    # rows est une liste de Row, on la convertit en liste de dict
    return [dict(r) for r in rows]

def get_users(id) -> List[Dict]:
    """Retourne la liste de tous les élèves."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users where id = ?;",(id,))
    rows = cur.fetchall()

    conn.close()

    # rows est une liste de Row, on la convertit en liste de dict
    return [dict(r) for r in rows]

def edit_users(id,name: str, wca: str,password:str,role:bool , icon :str) -> Dict:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE users SET name = ? , wca = ? , password = ? , role = ? , icon = ? WHERE id = ?;",(name , wca,password,role,icon , id))
    conn.commit()
    conn.close()
    return {"id": id, "name": name, "role": role, "icon": icon, "wca": wca, "password": password}

def add_users(name: str, wca: str,password:str,role:bool , icon :str) -> Dict:
    """Ajoute un élève et retourne ses informations."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (name, wca,password,role,icon) VALUES (?, ?, ?, ?, ?);",
        (name, wca, password, role, icon)
    )

    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return {"id": new_id, "name": name, "role": role, "icon": icon, "wca": wca, "password": password}

def del_users(id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE id = ?;", (id,))

        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return True
    except:
        return False

def get_users_by_name(name: str) -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users where name = ?;",(name,))

    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

edit_users(1,"Admin","2025JEAN01",hashlib.sha512((os.getenv("AP")).encode("utf-8")).hexdigest(),True,"https://avatars.worldcubeassociation.org/jhzj1xf5tpjnya82k08iyhg111xd")