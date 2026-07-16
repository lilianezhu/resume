import os
import sqlite3
from functools import wraps

from flask import Flask, g, redirect, render_template_string, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")

app = Flask(__name__)
app.secret_key = "dev-secret-key"


def get_db():
    if "db" not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """
    )
    db.commit()


with app.app_context():
    init_db()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


@app.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT posts.id, posts.content, posts.created_at, users.username FROM posts JOIN users ON users.id = posts.user_id ORDER BY posts.created_at DESC"
    ).fetchall()
    user_id = session.get("user_id")
    username = None
    if user_id is not None:
        username = db.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()["username"]
    return render_template_string(
        """
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Ocean Posts</title>
            <style>
                body {
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #e6f7ff 0%, #bfe7f8 45%, #7fc6d5 100%);
                    color: #10324a;
                }
                .shell {
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 32px 20px 48px;
                }
                .card {
                    background: rgba(255,255,255,0.88);
                    border-radius: 18px;
                    box-shadow: 0 10px 30px rgba(16,50,74,0.15);
                    padding: 24px;
                    margin-bottom: 20px;
                }
                h1, h2 { color: #0d4d6b; }
                .topbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
                .links a, .btn {
                    text-decoration: none;
                    color: #ffffff;
                    background: #2f8fb7;
                    padding: 8px 14px;
                    border-radius: 999px;
                    display: inline-block;
                    margin-right: 8px;
                }
                form textarea, form input {
                    width: 100%;
                    border: 1px solid #9fd5e3;
                    border-radius: 10px;
                    padding: 10px;
                    margin-top: 8px;
                    box-sizing: border-box;
                }
                button {
                    border: none;
                    border-radius: 999px;
                    padding: 9px 15px;
                    background: #0d4d6b;
                    color: white;
                    cursor: pointer;
                    margin-top: 8px;
                }
                .post {
                    border-left: 4px solid #2f8fb7;
                    padding: 12px 0 12px 12px;
                    margin-bottom: 10px;
                }
                .muted { color: #567a8b; font-size: 0.9em; }
            </style>
        </head>
        <body>
            <div class="shell">
                <div class="card">
                    <div class="topbar">
                        <h1>🌊 Ocean Posts</h1>
                        <div class="links">
                            <a href="/">Home</a>
                            {% if username %}
                                <span>Hello, {{ username }}!</span>
                                <a href="/logout">Logout</a>
                            {% else %}
                                <a href="/register">Register</a>
                                <a href="/login">Login</a>
                            {% endif %}
                        </div>
                    </div>
                    <p class="muted">A calm little space for sharing your thoughts by the tide.</p>
                    {% if username %}
                        <form method="post" action="/posts">
                            <textarea name="content" rows="3" placeholder="Write a new post..."></textarea><br>
                            <button type="submit">Post</button>
                        </form>
                    {% endif %}
                </div>
                <div class="card">
                    <h2>Recent Posts</h2>
                    {% for post in posts %}
                        <div class="post">
                            <strong>{{ post['username'] }}</strong>
                            <p>{{ post['content'] }}</p>
                            <div class="muted">{{ post['created_at'] }}</div>
                        </div>
                    {% endfor %}
                </div>
            </div>
        </body>
        </html>
        """,
        posts=posts,
        username=username,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        if not username or not password:
            error = "Username and password are required."
        else:
            db = get_db()
            existing = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
            if existing:
                error = "Username already exists."
            else:
                db.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
                return redirect(url_for("login"))
    return render_template_string(
        """
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Register</title>
            <style>
                body { margin: 0; font-family: Arial, sans-serif; background: linear-gradient(135deg, #e6f7ff 0%, #bfe7f8 45%, #7fc6d5 100%); color: #10324a; }
                .wrap { max-width: 420px; margin: 80px auto; padding: 24px; background: rgba(255,255,255,0.9); border-radius: 18px; box-shadow: 0 10px 30px rgba(16,50,74,0.15); }
                input { width: 100%; padding: 10px; border: 1px solid #9fd5e3; border-radius: 10px; margin-top: 8px; box-sizing: border-box; }
                button { margin-top: 12px; padding: 10px 14px; border: none; border-radius: 999px; background: #2f8fb7; color: white; cursor: pointer; }
                a { color: #0d4d6b; }
            </style>
        </head>
        <body>
            <div class="wrap">
                <h2>🌊 Create an account</h2>
                {% if error %}<p>{{ error }}</p>{% endif %}
                <form method="post">
                    <input name="username" placeholder="Username" /><br>
                    <input name="password" type="password" placeholder="Password" /><br>
                    <button type="submit">Register</button>
                </form>
                <p><a href="/">Back to home</a></p>
            </div>
        </body></html>
        """,
        error=error,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        error = "Invalid username or password."
    return render_template_string(
        """
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Login</title>
            <style>
                body { margin: 0; font-family: Arial, sans-serif; background: linear-gradient(135deg, #e6f7ff 0%, #bfe7f8 45%, #7fc6d5 100%); color: #10324a; }
                .wrap { max-width: 420px; margin: 80px auto; padding: 24px; background: rgba(255,255,255,0.9); border-radius: 18px; box-shadow: 0 10px 30px rgba(16,50,74,0.15); }
                input { width: 100%; padding: 10px; border: 1px solid #9fd5e3; border-radius: 10px; margin-top: 8px; box-sizing: border-box; }
                button { margin-top: 12px; padding: 10px 14px; border: none; border-radius: 999px; background: #2f8fb7; color: white; cursor: pointer; }
                a { color: #0d4d6b; }
            </style>
        </head>
        <body>
            <div class="wrap">
                <h2>🌊 Welcome back</h2>
                {% if error %}<p>{{ error }}</p>{% endif %}
                <form method="post">
                    <input name="username" placeholder="Username" /><br>
                    <input name="password" type="password" placeholder="Password" /><br>
                    <button type="submit">Login</button>
                </form>
                <p><a href="/">Back to home</a></p>
            </div>
        </body></html>
        """,
        error=error,
    )


@app.route("/posts", methods=["POST"])
@login_required
def create_post():
    content = request.form.get("content", "").strip()
    if content:
        db = get_db()
        db.execute("INSERT INTO posts (user_id, content) VALUES (?, ?)", (session["user_id"], content))
        db.commit()
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
