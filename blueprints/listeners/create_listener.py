from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class CreateListener(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])

    type = StringField('Type', default='HTTP')

    bind_address = StringField('Bind Address', default='0.0.0.0')
    
    bind_port = StringField('Bind Port', default='80')

    submit = SubmitField('Create') 


