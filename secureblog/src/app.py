from flask import Flask, render_template, request, redirect, session, g, Blueprint
import psycopg2
import os
import uuid
import hashlib
from datetime import datetime
import time


secureblog_bp = Blueprint('secureblog', 'secureblog')


def create_app():
    app = Flask(__name__)
    app.secret_key = 'BAD_SECRET_KEY'
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_DOMAIN"] = "secureblog.su"
    app.register_blueprint(secureblog_bp)
    return app


def get_db():
    if 'db' not in g:
        POSTGRES_USER = os.environ.get("POSTGRES_USER")
        POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
        POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
        POSTGRES_DBNAME = "blog"
        conn = psycopg2.connect(
            dbname=POSTGRES_DBNAME,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=5432,
            options='-c statement_timeout=300'
        )
        conn.set_session(autocommit=True)
        g.db = conn

    return g.db


def gen_acsrf():
    return str(uuid.uuid4())


def get_posts():
    with get_db().cursor() as cur:
        cur.execute("SELECT text, login FROM post;")
        return [(x[0], x[1]) for x in cur.fetchall()]


def create_post(post, login):
    with get_db().cursor() as cur:
        cur.execute(f"INSERT INTO post(text, login) VALUES ('{post}', '{login}');")


def get_user(login):
    with get_db().cursor() as cur:
        cur.execute(f"SELECT login, pwdhash FROM bloguser WHERE login = '{login}';")
        return next(iter(cur.fetchall()), None)


def create_user(login, password):
    result = get_user(login)
    if result is not None:
        return login
    pwdhash = hashlib.md5(password.encode()).hexdigest()
    try:
        with get_db().cursor() as cur:
            cur.execute(f"INSERT INTO bloguser(login, pwdhash) VALUES ('{login}', '{pwdhash}');")
    except:
        pass
    return login


@secureblog_bp.route("/")
def index():
    return render_template("index.html", posts=get_posts(), login=session.get("login"), acsrf=session.get("acsrf"))


@secureblog_bp.route("/posts", methods=["POST"])
def posts():
    if session.get("login") is not None:
        if request.form["acsrf"] == session.get("acsrf"):
            create_post(request.form["text"], session["login"])
        else:
            print("Wrong Anti CSRF token!", flush=True)
    return redirect("/")


@secureblog_bp.route("/users", methods=["POST"])
def users():
    start = datetime.now()
    try:
        created_login = create_user(request.form["login"], request.form["password"])
    except:
        created_login = request.form["login"]
    end = datetime.now()
    limit = 900
    past = (end - start).total_seconds() * 1000
    time.sleep((limit-past)/1000)
    return redirect(f"/login?auth_login={created_login}")


@secureblog_bp.route("/register", methods=["GET"])
def register():
    return render_template("register.html", login=session.get("login"))


@secureblog_bp.route("/login", methods=["GET", "POST"])
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


@secureblog_bp.route("/logout", methods=["GET"])
def logout():
    session.pop("login")
    return redirect("/")
