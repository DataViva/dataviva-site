# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, validators


class RegistrationForm(Form):
    profile = TextField('profile', validators=[
        validators.Required(u"Por favor, insira o título do post."),
        validators.Length(max=400)
    ])

    description = TextField('description', validators=[
        validators.Required(u"Por favor, insira o título do post."),
        validators.Length(max=400)
    ])

    selector = TextField('selector', validators=[
        validators.Required(u"Por favor, insira o(s) autor(es) do post."),
        validators.Length(max=100)
    ])

    answer = TextField('answer', validators=[
        validators.Required(u"Por favor, insira o título do post."),
        validators.Length(max=400)
    ])
