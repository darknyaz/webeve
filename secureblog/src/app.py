from flask import Flask, render_template, request, redirect, session
import psycopg2
import os
import uuid
import hashlib


app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
app.config["SESSION_COOKIE_DOMAIN"] = "secureblog.su"
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
conn.set_session(autocommit=True)


def gen_acsrf():
    return str(uuid.uuid4())


def get_posts():
    with conn.cursor() as cur:
        cur.execute("SELECT text, login FROM post;")
        return [(x[0], x[1]) for x in cur.fetchall()]


def create_post(post, login):
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO post(text, login) VALUES ('{post}', '{login}');")


def get_user(login):
    with conn.cursor() as cur:
        cur.execute(f"SELECT login, pwdhash FROM bloguser WHERE login = '{login}';")
        return next(iter(cur.fetchall()), None)


def create_user(login, password):
    result = get_user(login)
    if result is not None:
        return login
    pwdhash = hashlib.md5(password.encode()).hexdigest()
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO bloguser(login, pwdhash) VALUES ('{login}', '{pwdhash}');")
    return login


@app.route("/")
def index():
    return render_template("index.html", posts=get_posts(), login=session.get("login"), acsrf=session.get("acsrf"))


@app.route("/posts", methods=["POST"])
def posts():
    if session.get("login") is not None:
        if request.form["acsrf"] == session.get("acsrf"):
            create_post(request.form["text"], session["login"])
        else:
            print("Wrong Anti CSRF token!", flush=True)
    return redirect("/")


@app.route("/users", methods=["POST"])
def users():
    created_login = create_user(request.form["login"], request.form["password"])
    return redirect(f"/login?auth_login={created_login}")


@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html", login=session.get("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", login=session.get("login"), auth_login=request.args.get("auth_login"))
    login = request.form["login"]
    password = request.form["password"]
    login_pwdhash_db = get_user(login)
    if login_pwdhash_db is not None:
        _, pwdhash_db = login_pwdhash_db
        actual_pwdhash = hashlib.md5(password.encode()).hexdigest()
        if pwdhash_db != actual_pwdhash:
            return render_template("login.html", login=session.get("login"))
        session['login'] = login
        session['acsrf'] = gen_acsrf()
    return redirect("/") 


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("login")
    return redirect("/")
