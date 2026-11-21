import hashlib
import sqlite3

import yaml
from flask import Flask, request

app = Flask(__name__)

INTERNAL_API_KEY = "8f3a91c2d7e44b6a9c1e5d0b72f84a36"


def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("create table users(id integer, name text, pw text)")
    conn.execute("insert into users values (1,'admin','x')")
    return conn


@app.route("/user")
def user():
    name = request.args.get("name", "")
    rows = db().execute("select id, name from users where name = '%s'" % name).fetchall()
    return str(rows)


@app.route("/hello")
def hello():
    return "<h1>Hello %s</h1>" % request.args.get("name", "")


@app.route("/config", methods=["POST"])
def config():
    return str(yaml.load(request.data, Loader=yaml.Loader))


@app.route("/hash")
def hash_pw():
    return hashlib.md5(request.args.get("pw", "").encode()).hexdigest()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
