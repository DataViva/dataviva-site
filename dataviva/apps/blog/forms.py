# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import FileField, TextField, TextAreaField, validators, ValidationError


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
    title = TextField('title', [validators.Required(u"Por favor, insira o título do post."), validators.Length(max=400)])
    author = TextField('author', [validators.Required(u"Por favor, insira o(s) autor(es) do post."), validators.Length(max=50)])
    category = TextField('category', [validators.Required(u"Por favor, insira a categoria do post.")])
    text = TextAreaField('text', [validators.Required(u"Por favor, insira o texto do post."), NumberOfWords(max=500)])
    image = FileField('image', [validators.Required(u"Por favor, insira a image do post.")])
    thumb = FileField('thumb', [validators.Required(u"Por favor, insira o thumb do post.")])
