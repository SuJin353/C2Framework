from flask import Blueprint, render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

payload_bp = Blueprint('payload', __name__, template_folder='templates', static_folder='static')

class GeneratePayload(FlaskForm):
    listener = StringField('Listener', [validators.DataRequired()])

    type = StringField('Type', default='Power Shell')

    submit = SubmitField('Generate')


@payload_bp.route('/', methods=['GET', 'POST'])
def payload():
    form = GeneratePayload(request.form)
    return render_template('payload.html', form = form)
