from flask import (
    Flask, render_template, send_from_directory, redirect, request,
    url_for, Blueprint, current_app
)
import os


evilsite_bp = Blueprint('evilsite', 'evilsite')


def create_app():
    app = Flask(__name__)
    app.register_blueprint(evilsite_bp)
    return app


UPLOADS_FOLDERNAME = "uploads"
UPLOADS_FOLDERPATH=os.path.join('/app', UPLOADS_FOLDERNAME)


def get_upload_urls():
    result = []
    for file in os.listdir(UPLOADS_FOLDERPATH):
        result.append(f'{UPLOADS_FOLDERNAME}/{file}')
    return result


@evilsite_bp.route("/")
def index():
    return render_template('index.html', urls=get_upload_urls())

@evilsite_bp.route(f"/{UPLOADS_FOLDERNAME}/<path:name>")
def download_file(name):
    return send_from_directory(UPLOADS_FOLDERNAME, name)

@evilsite_bp.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and file.filename:
            file.save(os.path.join(UPLOADS_FOLDERPATH, file.filename))
            return redirect(url_for('evilsite.download_file', name=file.filename))
    return render_template('upload.html')
