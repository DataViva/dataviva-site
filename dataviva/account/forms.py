from flask_wtf import Form
from wtforms import TextField, TextAreaField, BooleanField, HiddenField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import URLField

from dataviva.ask.models import Status

class LoginForm(Form):
    provider = HiddenField('provider', validators = [validators.Required()])
    remember_me = BooleanField('remember_me', default = False)

class UserEditForm(Form):
    nickname = TextField('nickname', validators = [validators.Required()])
    bio = TextAreaField('bio', validators = [validators.Length(min=0, max=256)])
    website = URLField(validators=[validators.url()])
