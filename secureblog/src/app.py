from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!<br>secret: one_billon_dollar_information</p>"

