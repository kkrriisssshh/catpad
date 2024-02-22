import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def create_upload_folder_if_not_exists():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

@app.route("/notes", methods=["POST"])
def notes():
    create_upload_folder_if_not_exists()
    
    if "title" not in request.form or "note" not in request.form:
        flash("title or note is missing")
        return redirect(request.url)
    
    title = request.form["title"]
    note = request.form["note"]
    
    if title.strip() == "":
        flash("title cannot be empty")
        return redirect(request.url)
    
    if note.strip() == "":
        flash("note cannot be empty")
        return redirect(request.url)

    filename = secure_filename(title + ".txt")
    with open(os.path.join(app.config["UPLOAD_FOLDER"], filename), "w") as f:
        f.write(note)
    
    return redirect(url_for("home"))

@app.route("/")
def home(name=None):
    create_upload_folder_if_not_exists()
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("index.html", name=name)

if __name__ == "__main__":
    app.run(debug=True)