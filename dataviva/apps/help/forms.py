# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import HiddenField, SelectField, TextField, validators
from models import HelpSubject


class RegistrationForm(Form):

    #TODO - Get PT-Lang categories names
    category = SelectField('category', choices=[(category.id, category.name_en) for category in HelpSubject.query.order_by('name_en')], validators=[
        validators.Required(u"Por favor, selecione a categoria.")])

    description_en = TextField('description_en', validators=[
        validators.Required(u"Por favor, insira a pergunta em inglês."),
        validators.Length(max=400)
    ])

    description_pt = TextField('description_pt', validators=[
        validators.Required(u"Por favor, insira a pergunta em português."),
        validators.Length(max=400)
    ])

    answer_en = HiddenField('answer_en', validators=[
        validators.Required(u"Por favor, insira a resposta em inglês."),
        validators.Length(max=400)
    ])

    answer_pt = HiddenField('answer_pt', validators=[
        validators.Required(u"Por favor, insira a resposta em português."),
        validators.Length(max=400)
    ])
