# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, HiddenField, validators, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired

IMAGES = ('png', 'jpeg', 'jpg')


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
        validators.Required(u"Por favor, insira a categoria do post.")
    ])

    text_content = HiddenField('text_content', validators=[
        validators.Required(u"Por favor, insira o texto do post.")
    ])

    image = FileField('featured-image', validators=[
        FileAllowed(IMAGES, 'Images only!')
    ])

    thumb = FileField('thumb-image', validators=[
        FileRequired(u"Por favor, insira o thumb do post."),
        FileAllowed(IMAGES, 'Images only!')
    ])
