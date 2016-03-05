from flask_wtf import Form
from wtforms import TextField, TextAreaField, BooleanField, HiddenField, validators
from wtforms.fields.html5 import URLField


class SignupForm(Form):
    email = TextField('email', validators=[validators.Required(), validators.Email()])
    fullname = TextField('fullname', validators=[validators.Required(),
                                                 validators.Length(min=3, max=128)])
    password = TextField('password', validators=[validators.Required(),
                                                 validators.EqualTo(
                                                    'confirm',
                                                    message='Passwords must match')])
    confirm = TextField('confirm', validators=[validators.Required()])


class LoginForm(Form):
    provider = HiddenField('provider', validators=[validators.Required()])
    remember_me = BooleanField('remember_me', default=False)


class UserEditForm(Form):
    nickname = TextField('nickname', validators=[validators.Required()])
    bio = TextAreaField('bio', validators=[validators.Length(min=0, max=256)])
    website = URLField(validators=[validators.url()])
