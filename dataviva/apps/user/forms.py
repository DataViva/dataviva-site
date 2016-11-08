from flask_wtf import Form
from wtforms import TextField, DateField, BooleanField, HiddenField, validators, PasswordField, SelectField


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
    fullname = TextField('fullname', validators=[validators.Required(), validators.Length(min=3, max=128, message='Name field must be between 3 and 128 characters long.')])
    email = TextField('email', validators=[validators.Required(), validators.Email()])
    birthday = DateField('birthday', validators=[ validators.Required()],format='%d/%m/%Y', description='Date format: day/month/year')
    country = TextField('country', validators=[validators.Required(), validators.Length(max=50, message='Country field must be 50 characters long.')])
    state_province_region = TextField('state_province_region', validators=[validators.Required(), validators.Length( max=50, message='Format error.')])
    city = TextField('city', validators=[validators.Required(), validators.Length(max=50, message='City field must be 50 characters long.')])
    profile = SelectField('gender', choices=[('development_agents', 'Development Agents'),('entrepreneurs', 'Entrepreneurs'), ('students', 'Students and Professionals')])
    occupation = TextField('occupation', validators=[validators.Required(), validators.Length(max=50, message='Occupation field must be 50 characters long.')])
    institution = TextField('institution', validators=[validators.Optional(), validators.Length(max=50, message='Institution field must be 50 characters long.')])
    agree_mailer = BooleanField('agree_mailer')
