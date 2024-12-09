from flask_wtf import FlaskForm
from wtforms import StringField

class AgentInfo(FlaskForm):
    listener_name = StringField('Listener')

    listener_type = StringField('Listener Type')

    bind_address = StringField('Bind Address')

    bind_port = StringField('Bind Port')

    agent_type = StringField('Agent Type')

    remote_address = StringField('Remote Address')

    hostname = StringField('Host Name')

    sleep = StringField('Sleep')


