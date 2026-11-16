import getpass
import sqlite3
import sys

import bcrypt

from app import db


def ask_password():
    password = getpass.getpass("Password: ")
    if password != getpass.getpass("Repeat password: "):
        sys.exit("Passwords do not match")
    if len(password) < 6:
        sys.exit("Password must be at least 6 characters")
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def add_user(username):
    password_hash = ask_password()
    try:
        with db() as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )
    except sqlite3.IntegrityError:
        sys.exit(f"User '{username}' already exists")
    print(f"User '{username}' created")


def change_password(username):
    password_hash = ask_password()
    with db() as conn:
        cur = conn.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?",
            (password_hash, username),
        )
        if cur.rowcount == 0:
            sys.exit(f"User '{username}' not found")
        conn.execute(
            "DELETE FROM sessions WHERE user_id = (SELECT id FROM users WHERE username = ?)",
            (username,),
        )
    print(f"Password for '{username}' changed")


def list_users():
    with db() as conn:
        for row in conn.execute("SELECT username FROM users ORDER BY id"):
            print(row["username"])


COMMANDS = {"adduser": add_user, "passwd": change_password}

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "list":
        list_users()
    elif len(sys.argv) == 3 and sys.argv[1] in COMMANDS:
        COMMANDS[sys.argv[1]](sys.argv[2])
    else:
        sys.exit("Usage: manage.py adduser|passwd <username> | manage.py list")