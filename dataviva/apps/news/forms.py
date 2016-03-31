# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import HiddenField, TextField, TextAreaField, validators


class RegistrationForm(Form):
    title = TextField('title', validators=[
        validators.Required(u"Por favor, insira o título da notícia."),
        validators.Length(max=400)
    ])

    authors = TextField('authors', validators=[
        validators.Required(u"Por favor, insira o(s) autor(es) da notícia."),
        validators.Length(max=100)
    ])

    subject = TextField('subject', validators=[
        validators.Required(u"Por favor, insira a categoria da notícia.")
    ])

    text_call = TextAreaField('text_call', validators=[
        validators.Required(u"Por favor, insira uma chamada para a notícia."),
        validators.Length(max=500)
    ])

    text_content = HiddenField('text_content', validators=[
        validators.Required(u"Por favor, insira o conteúdo da notícia.")
    ])

    thumb = HiddenField('thumb', validators=[
        validators.Required(u"Por favor, insira uma imagem para a chamada.")
    ])
