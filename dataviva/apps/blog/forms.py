# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import HiddenField, TextField, TextAreaField, validators


class RegistrationForm(Form):
    title = TextField('title', validators=[
        validators.Required(u"Por favor, insira o título do post."),
        validators.Length(max=400)
    ])

    authors = TextField('authors', validators=[
        validators.Required(u"Por favor, insira o(s) autor(es) do post."),
        validators.Length(max=100)
    ])

    subject = TextField('subject', validators=[
        validators.Required(u"Por favor, insira a categoria do post.")
    ])

    text_call = TextAreaField('text_call', validators=[
        validators.Required(u"Por favor, insira uma chamada para o post."),
        validators.Length(max=500)
    ])

    text_content = HiddenField('text_content', validators=[
        validators.Required(u"Por favor, insira o conteúdo do post.")
    ])

    thumb = HiddenField('thumb', validators=[
        validators.Required(u"Por favor, insira uma imagem para a chamada.")
    ])
