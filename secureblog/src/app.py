from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_DBNAME = "blog"
conn = psycopg2.connect(
    dbname=POSTGRES_DBNAME,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=5432
)

def get_posts():
    with conn.cursor() as cur:
        cur.execute("SELECT text, login FROM post;")
        return [(x[0], x[1]) for x in cur.fetchall()]


def create_post(post, login):
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO post(text, login) VALUES ('{post}', '{login}');")


def get_user(login):
    with conn.cursor() as cur:
        cur.execute(f"SELECT login FROM bloguser WHERE login = '{login}';")
        return next(iter(cur.fetchall()), [None])[0]


def create_user(login):
    if get_user(login) is not None:
        return
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO bloguser(login) VALUES ('{login}');")


@app.route("/")
def index():
    return render_template("index.html", posts=get_posts(), login=session.get("login"))


@app.route("/posts", methods=["POST"])
def posts():
    if session.get("login") is not None:
        create_post(request.form["text"], session["login"])
    return redirect("/")


@app.route("/users", methods=["POST"])
def users():
    create_user(request.form["login"])
    return redirect("/login")


@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html", login=session.get("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", login=session.get("login"))
    login = request.form["login"]
    if get_user(login) is not None:
        session['login'] = login
    return redirect("/") 


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("login")
    return redirect("/")
