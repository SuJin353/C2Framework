from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired

class CreateListener(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

    bind_address = StringField('Bind Address', default='0.0.0.0', validators=[DataRequired()])
    
    bind_port = StringField('Bind Port', default='80', validators=[DataRequired()])
    
    connect_address = StringField('Connect Address', default='10.10.5.205', validators=[DataRequired()])
    
    connect_port = StringField('Connect Port', default='80', validators=[DataRequired()])
    
    use_ssl = SelectField('Use SSL', choices=[('false', 'False'), ('true', 'True')])
    
    http_profile = SelectField('HTTP Profile', choices=[('CustomHttpProfile', 'CustomHttpProfile')])
    
    submit = SubmitField('Create')
