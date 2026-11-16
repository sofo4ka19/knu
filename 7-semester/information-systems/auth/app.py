import os
import sqlite3
import secrets

import bcrypt
from flask import Flask, request, redirect, make_response, render_template_string

DB_PATH = os.getenv("AUTH_DB_PATH", "/data/auth.db")
SESSION_COOKIE = "session_id"

app = Flask(__name__)

LOGIN_PAGE = """
<!doctype html>
<title>Login</title>
<h2>Sign in</h2>
{% if error %}<p style="color:red">{{ error }}</p>{% endif %}
<form method="post">
  <input name="username" placeholder="Username" required><br>
  <input name="password" type="password" placeholder="Password" required><br>
  <button type="submit">Sign in</button>
</form>
"""


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    admin_user = os.getenv("AUTH_ADMIN_USER")
    admin_pass = os.getenv("AUTH_ADMIN_PASSWORD")
    if admin_user and admin_pass:
        with db() as conn:
            exists = conn.execute(
                "SELECT 1 FROM users WHERE username = ?", (admin_user,)
            ).fetchone()
            if not exists:
                conn.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (admin_user, bcrypt.hashpw(admin_pass.encode(), bcrypt.gensalt())),
                )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template_string(LOGIN_PAGE, error=None)
    username = request.form["username"]
    password = request.form["password"].encode()
    with db() as conn:
        user = conn.execute(
            "SELECT id, password_hash FROM users WHERE username = ?", (username,)
        ).fetchone()
        if not user or not bcrypt.checkpw(password, user["password_hash"]):
            return render_template_string(LOGIN_PAGE, error="Invalid credentials"), 401
        token = secrets.token_urlsafe(32)
        conn.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token, user["id"]))
    resp = make_response(redirect("/"))
    resp.set_cookie(SESSION_COOKIE, token, httponly=True, samesite="Lax")
    return resp


@app.route("/logout")
def logout():
    token = request.cookies.get(SESSION_COOKIE)
    if token:
        with db() as conn:
            conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
    resp = make_response(redirect("/login"))
    resp.delete_cookie(SESSION_COOKIE)
    return resp


@app.route("/verify")
def verify():
    token = request.cookies.get(SESSION_COOKIE)
    if token:
        with db() as conn:
            row = conn.execute(
                """SELECT u.username FROM sessions s
                   JOIN users u ON u.id = s.user_id WHERE s.token = ?""",
                (token,),
            ).fetchone()
        if row:
            resp = make_response("", 200)
            resp.headers["X-Auth-User"] = row["username"]
            return resp
    return "", 401


@app.route("/health")
def health():
    return "ok"


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)