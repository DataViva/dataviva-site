# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, validators
from models import SearchProfile


class RegistrationForm(Form):

    profile = SelectField('profile', coerce=int, choices=[(profile.id, profile.name) for profile in SearchProfile.query.order_by('name')], validators=[
        validators.Required(u"Por favor, selecione o profile.")])

    description = TextField('description', validators=[
        validators.Required(u"Por favor, insira a pergunta."),
        validators.Length(max=400)
    ])

    selector = TextField('selector', validators=[
        validators.Required(u"Por favor, insira o(s) seletores(es) da pesquisa."),
        validators.Length(max=100)
    ])

    answer = TextField('answer', validators=[
        validators.Required(u"Por favor, insira a resposta da pesquisa."),
        validators.Length(max=400)
    ])
