from email.policy import default

from flask_wtf import FlaskForm
from wtforms import StringField

class Tasks(FlaskForm):
    tasks = StringField('Tasks', default = "")