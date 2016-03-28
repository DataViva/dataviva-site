# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import HiddenField, TextField, TextAreaField, validators, ValidationError


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
            u"Por favor, insira o título do post."), validators.Length(max=400)
    ])

    authors = TextField('authors', validators=[
        validators.Required(
            u"Por favor, insira o(s) autor(es) do post."), validators.Length(max=100)
    ])

    subject = TextField('subject', validators=[
        validators.Required(
            u"Por favor, insira a categoria do post.")
    ])

    text_content = HiddenField('text_content', validators=[
        validators.Required(
            u"Por favor, insira o texto do post."), NumberOfWords(max=500)
    ])

    text_call = TextAreaField('subject', validators=[
        validators.Required(u"Por favor, insira uma chamada para o post."), NumberOfWords(max=500)
    ])

    image = HiddenField('image')

    thumb = HiddenField('thumb', validators=[
        validators.Required(u"Por favor, insira uma imagem reduzida.")
    ])
