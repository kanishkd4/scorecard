from flask import render_template
from app import app
from flask_wtf import Form
from flask_wtf.file import FileField
from werkzeug import secure_filename
from wtforms import StringField
from wtforms.validators import DataRequired
import pandas as pd
from Scorecard import scorecard

class UploadForm(Form):
    file = FileField(label="~ separted file path to load", validators=[DataRequired()])
    target = StringField(label="target", validators=[DataRequired()])

@app.route("/")
@app.route("/loaddata", methods=["GET"])
def load():
    form = UploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        base = pd.read_table(filename, sep="~")
        score = scorecard(modelbase=base, target=form.target)
        var_start_list = score.univariate().to_html()
    return render_template("loaddata.html", title="Load data to create scorecard", var_start_list=var_start_list, form=form)