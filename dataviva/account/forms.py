from flask.ext.wtf import Form, TextField, TextAreaField, BooleanField, QuerySelectField, HiddenField
from flask.ext.wtf import Required, Length, url
from flask.ext.wtf.html5 import URLField

from dataviva.ask.models import Status

class LoginForm(Form):
    provider = HiddenField('provider', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class UserEditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    bio = TextAreaField('bio', validators = [Length(min=0, max=256)])
    website = URLField(validators=[url()])
