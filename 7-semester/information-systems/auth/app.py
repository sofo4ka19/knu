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
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Вхід — моніторинг БД</title>
<style>
  :root { --bg:#111217; --card:#1b1d24; --line:#2c2f3a; --text:#e6e8ee; --muted:#8b91a3; --accent:#5794f2; --err:#f2495c; }
  * { box-sizing: border-box; }
  body { margin:0; min-height:100vh; display:grid; place-items:center; background:var(--bg); color:var(--text);
         font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
  .card { width:min(380px, 92vw); background:var(--card); border:1px solid var(--line); border-radius:12px; padding:32px 28px; }
  h1 { margin:0 0 4px; font-size:22px; }
  p.sub { margin:0 0 24px; color:var(--muted); font-size:14px; }
  label { display:block; margin:14px 0 6px; font-size:13px; color:var(--muted); }
  input { width:100%; padding:11px 12px; border-radius:8px; border:1px solid var(--line); background:var(--bg);
          color:var(--text); font-size:15px; }
  input:focus { outline:2px solid var(--accent); border-color:transparent; }
  button { width:100%; margin-top:22px; padding:12px; border:0; border-radius:8px; background:var(--accent);
           color:#fff; font-size:15px; font-weight:600; cursor:pointer; }
  button:hover { filter:brightness(1.1); }
  .error { margin-top:16px; padding:10px 12px; border-radius:8px; background:rgba(242,73,92,.12);
           border:1px solid var(--err); color:#ff9aa6; font-size:14px; }
</style>
</head>
<body>
  <form class="card" method="post" action="/login">
    <h1>Моніторинг БД</h1>
    <p class="sub">Увійдіть, щоб відкрити дашборд</p>

    <label for="u">Логін</label>
    <input id="u" name="username" autocomplete="username" autofocus required>

    <label for="p">Пароль</label>
    <input id="p" name="password" type="password" autocomplete="current-password" required>

    {% if error %}<div class="error">{{ error }}</div>{% endif %}

    <button type="submit">Увійти</button>
  </form>
</body>
</html>
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