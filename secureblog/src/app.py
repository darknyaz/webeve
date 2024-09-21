from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)
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
#conn.set_session(autocommit=True)

def get_posts():
    with conn.cursor() as cur:
        cur.execute("SELECT text FROM post;")
        return [x[0] for x in cur.fetchall()]


def create_post(post):
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO post(text) VALUES ('{post}');")


@app.route("/")
def index():
    return render_template("index.html", posts=get_posts())


@app.route("/posts", methods=["POST"])
def posts():
    create_post(request.form["text"])
    return redirect("/")
