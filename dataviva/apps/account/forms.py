from flask_wtf import Form
from wtforms import TextField, TextAreaField, BooleanField, HiddenField, validators, PasswordField, SelectField
from wtforms.fields.html5 import URLField


class SignupForm(Form):
    email = TextField('email', validators=[validators.Required(), validators.Email()])
    fullname = TextField('fullname', validators=[validators.Required(),
                                                    validators.Length(min=3, max=128,
                                                    message='Name field must be between 3 and 128 characters long.')])
    password = PasswordField('password', validators=[validators.Required(),
                                                        validators.EqualTo('confirm',
                                                        message='Passwords must match')])
    confirm = PasswordField('confirm', validators=[validators.Required()])
    agree_mailer = BooleanField('agree_mailer')


class SigninForm(Form):
    email = TextField('email', validators=[validators.Required(), validators.Email()])
    password = PasswordField('password', validators=[validators.Required()])


class ChangePasswordForm(Form):
    current_password = PasswordField('current_password', validators=[validators.Required()])
    new_password = PasswordField('new_password', validators=[validators.Required()])
    confirm = PasswordField('confirm', validators=[validators.Required(), validators.EqualTo(
        'new_password', message='Passwords must match')])


class LoginForm(Form):
    provider = HiddenField('provider', validators=[validators.Required()])
    remember_me = BooleanField('remember_me', default=False)


class ForgotPasswordForm(Form):
    email = TextField('email', validators=[validators.Required(), validators.Email()])


class ProfileForm(Form):
    fullname = TextField('fullname', validators=[validators.Required(),
                                                    validators.Length(min=3, max=128,
                                                    message='Name field must be between 3 and 128 characters long.')])
    gender = SelectField('gender', choices=[('male', 'Male'), ('female', 'Female')])
    email = TextField('email', validators=[validators.Required(), validators.Email()])
    country = TextField('country', validators=[validators.Required()])
    

    website = TextField('website', validators=[validators.Optional(), validators.URL(), validators.Length(min=10, max=150)])
    bio = TextField('bio', validators=[validators.Length(max=256)])
