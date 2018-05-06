
import os
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd
from flask import send_from_directory
from app import app
from app.Scorecard import scorecard

ALLOWED_EXTENSIONS = set(["txt"])
def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

class TargetForm(FlaskForm):
    target = StringField(label="target", validators=[DataRequired()])
    submit = SubmitField("submit")

@app.route("/", methods=["GET", "POST"])
def upload_file():
    form = TargetForm()
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("uploaded_file",
                                    filename=filename, y=form.target.data))
    return render_template("loaddata.html", form=form)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    base = pd.read_table(f"{app.config['UPLOAD_FOLDER']}/{filename}", sep="~")
    score = scorecard(modelBase=base, target="y")
    score.univariate()
    return score.var_start_list.to_html()
