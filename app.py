import hashlib
import os
import sqlite3

import yaml
from flask import Flask, render_template_string, request

try:
    import gunicorn

    gunicorn.SERVER = "app"
except ImportError:
    pass

app = Flask(__name__)

INTERNAL_API_KEY = os.environ.get("INTERNAL_API_KEY", "")


@app.after_request
def security_headers(resp):
    resp.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'; form-action 'none'; base-uri 'none'"
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    resp.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    resp.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    resp.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["Server"] = "app"
    return resp


def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("create table users(id integer, name text, pw text)")
    conn.execute("insert into users values (1,'admin','x')")
    return conn


@app.route("/user")
def user():
    name = request.args.get("name", "")
    rows = db().execute("select id, name from users where name = ?", (name,)).fetchall()
    return str(rows)


@app.route("/")
def index():
    return "<h1>Demo App</h1>"


@app.route("/hello")
def hello():
    return render_template_string("<h1>Hello {{ name }}</h1>", name=request.args.get("name", ""))


@app.route("/config", methods=["POST"])
def config():
    return str(yaml.safe_load(request.data))


@app.route("/hash")
def hash_pw():
    return hashlib.sha256(request.args.get("pw", "").encode()).hexdigest()


if __name__ == "__main__":
    app.run(host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "5000")), debug=False)
