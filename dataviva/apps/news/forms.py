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
    authors= TextField('authors', [validators.Required(u"Por favor, insira o(s) autor(es) do post."), validators.Length(max=100)])
    subject = TextField('subject', [validators.Required(u"Por favor, insira a categoria do post.")])
    text_content = TextAreaField('text_content', [validators.Required(u"Por favor, insira o texto do post."), NumberOfWords(max=500)])
    image_path = FileField('image_path', [validators.Required(u"Por favor, insira a imagem do post.")])
    thumb_path = FileField('thumb_path', [validators.Required(u"Por favor, insira o thumb do post.")])
