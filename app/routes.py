from flask import render_template, redirect, url_for
from flask_wtf import Form
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd
from app import app
# from Scorecard import scorecard

class UploadForm(Form):
    file = StringField(label="'~' separted file path to load", validators=[DataRequired()])
    target = StringField(label="target", validators=[DataRequired()])
    submit = SubmitField("Create univariate")

@app.route("/")
@app.route("/loaddata", methods=["GET", "POST"])
def load():
    form = UploadForm()
    if form.validate_on_submit():
        base = pd.read_table(form.file, sep="~")
        score = scorecard(modelbase=base, target=form.target)
        var_start_list = score.univariate().to_html()
        # return redirect(url_for("/show_output.html"))
    return render_template("loaddata.html", title="Load data to create scorecard", form=form)


# @app.route("/show_outupt")
# def show_output(var_start_list):
