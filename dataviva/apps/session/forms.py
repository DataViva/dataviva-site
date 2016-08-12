from flask_wtf import Form
from wtforms import TextField, PasswordField, validators


class LoginForm(Form):
    email = TextField('email', validators=[validators.Required(), validators.Email()])
    password = PasswordField('password', validators=[validators.Required()])
