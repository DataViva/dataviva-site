# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextAreaField, TextField, HiddenField, validators, ValidationError


class NumberOfWords(object):

    def __init__(self, max, message=None):
        self.max = max
        if not message:
            message = u"Campo deve possuir no máximo %d palavras." % (max)
        self.message = message

    def __call__(self, form, field):
        if len(field.data.split()) > self.max:
            raise ValidationError(self.message)


class RegistrationForm(Form):
    title = TextField('title', validators=[
        validators.Required(
            u"Por favor, insira o título da notícia."), validators.Length(max=400)
    ])

    authors = TextField('authors', validators=[
        validators.Required(
            u"Por favor, insira o(s) autor(es) da notícia."), validators.Length(max=100)
    ])

    subject = TextField('subject', validators=[
        validators.Required(u"Por favor, insira a categoria da notícia.")
    ])

    text_call = TextAreaField('subject', validators=[
        validators.Required(u"Por favor, insira uma chamada para a notícia."),
        NumberOfWords(max=500)
    ])

    text_content = HiddenField('text_content', validators=[
        validators.Required(u"Por favor, insira o conteúdo da notícia.")
    ])

    image = HiddenField('image')

    thumb = HiddenField('thumb', validators=[
        validators.Required(u"Por favor, insira uma imagem reduzida.")
    ])
