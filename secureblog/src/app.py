from flask import Flask
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

@app.route("/")
def hello_world():
    return "<p>Hello, World!<br>secret: one_billon_dollar_information</p>"


