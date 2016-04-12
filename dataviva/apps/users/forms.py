# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import HiddenField, TextField, TextAreaField, validators, SelectField


class RegistrationForm(Form):
    nickname = TextField('nickname', validators=[
        validators.Required(u"Por favor, insira o apelido do usuário."),
        validators.Length(max=64)
    ])

    email = TextField('email', validators=[
        validators.Required(u"Por favor, insira o e-mail do usuário."),
        validators.Length(max=120)
    ])

    fullname = TextField('fullname', validators=[
        validators.Required(u"Por favor, insira o nome completo do usuário."),
        validators.Length(max=200)
    ])

    country = TextField('country', validators=[
        validators.Required(u"Por favor, insira a localidade do usuário."),
        validators.Length(max=80)
    ])

    gender = SelectField(choices=[('male', 'Masculino'), ('female', 'Feminino')], validators=[
        validators.Required(u"Por favor, insira a localidade do usuário."),
        validators.Length(max=10)
    ])
