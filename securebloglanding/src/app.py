from flask import Flask, render_template, request
import json
import base64

app = Flask(__name__)


def pad_b64(s):
    return s + "=" * ((4 - len(s) % 4) % 4)


def get_login(request):
    session = request.args.get("session")
    if session is None:
        session = request.cookies.get("session")
    if session is None:
        return None
    payload_b64 = session.split(".", 1)[0]
    payload = base64.b64decode(pad_b64(payload_b64))
    payload_d = json.loads(payload)
    return payload_d["login"]


@app.route("/")
def index():
    return render_template("index.html", login=get_login(request))
