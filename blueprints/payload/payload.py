from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,validators
from ..listeners.listeners import load_listeners, Listener

payload_bp = Blueprint('payload', __name__, template_folder='templates', static_folder='static')

class GeneratePayload(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])

    listener = SelectField('Listener', validators=[validators.DataRequired()])

    type = StringField('Type', default='Power Shell')

    submit = SubmitField('Generate')

def generate_payload(listener, name):
    out_path = "source_payload/output/{}.ps1".format(name)
    ip = listener[3]
    port = listener[4]
    with open("source_payload/powershell.ps1", "rt") as p:
        payload = p.read()

    payload = payload.replace('REPLACE_IP', ip)
    payload = payload.replace('REPLACE_PORT', str(port))

    with open(out_path, "wt") as f:
        f.write(payload)

@payload_bp.route('/', methods=['GET', 'POST'])
def payload():
    listener_list = load_listeners()
    form = GeneratePayload(request.form)
    if form.is_submitted():
        name = form.name.data
        selected_listener = request.form.get('listener_select')
        for listener in listener_list:
            if listener[0] == selected_listener:
                generate_payload(listener, name)
    return render_template('payload.html', form = form, listeners = listener_list)
