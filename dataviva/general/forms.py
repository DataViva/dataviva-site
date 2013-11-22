from flask_wtf import Form
from wtforms import PasswordField

class AccessForm(Form):
    pw = PasswordField('pw')