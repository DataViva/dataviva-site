# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import HiddenField, SelectField, TextField, validators
from models import HelpSubject


class RegistrationForm(Form):

    subject = SelectField('subject', validators=[
        validators.Required(u"Por favor, selecione a categoria.")])

    def subject_choices(self, lang):
        name = 'name_'+lang
        self.subject.choices = [(str(subject.id), subject.name()) for subject in HelpSubject.query.order_by(name)]

    description_en = TextField('description_en', validators=[
        validators.Required(u"Por favor, insira a pergunta em inglês."),
        validators.Length(max=200)
    ])

    description_pt = TextField('description_pt', validators=[
        validators.Required(u"Por favor, insira a pergunta em português."),
        validators.Length(max=200)
    ])

    answer_en = HiddenField('answer_en', validators=[
        validators.Required(u"Por favor, insira a resposta em inglês.")
    ])

    answer_pt = HiddenField('answer_pt', validators=[
        validators.Required(u"Por favor, insira a resposta em português.")
    ])
