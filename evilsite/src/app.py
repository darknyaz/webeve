from flask import (
    Flask, render_template, send_from_directory, redirect, request,
    url_for
)
import os


app = Flask(__name__)

UPLOADS_FOLDERNAME = "uploads"
UPLOADS_FOLDERPATH=os.path.join(app.root_path, UPLOADS_FOLDERNAME)


def get_upload_urls():
    result = []
    for file in os.listdir(UPLOADS_FOLDERPATH):
        result.append(f'{UPLOADS_FOLDERNAME}/{file}')
    return result


@app.route("/")
def index():
    return render_template('index.html', urls=get_upload_urls())

@app.route(f"/{UPLOADS_FOLDERNAME}/<path:name>")
def download_file(name):
    return send_from_directory(UPLOADS_FOLDERNAME, name)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and file.filename:
            file.save(os.path.join(UPLOADS_FOLDERPATH, file.filename))
            return redirect(url_for('download_file', name=file.filename))
    return render_template('upload.html')
