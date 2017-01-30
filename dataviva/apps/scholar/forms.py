# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, HiddenField, validators, ValidationError
from dataviva.utils.custom_fields import TagsField
from models import KeyWord, Article


class NumberOfWords(object):

    def __init__(self, max, message=None):
        self.max = max
        if not message:
            message = u"Campo deve possuir no máximo %d palavras." % (max)
        self.message = message

    def __call__(self, form, field):
        if len(field.data.split()) > self.max:
            raise ValidationError(self.message)


def validate_keywords(form, field):
    if len(field.data) > 3:
        raise ValidationError(u"Por favor, insira no máximo três palavras-chave para o artigo.")


class RegistrationForm(Form):
    title = TextField('title', validators=[
        validators.Required(u"Por favor, insira o título do artigo."),
        validators.Length(max=400)
    ])

    theme = TextField('theme', validators=[
      validators.Required(u"Por favor, insira o tema do artigo."),
      NumberOfWords(max=5)
    ])

    authors = TextField('authors', validators=[
        validators.Required(u"Por favor, insira o(s) autor(es) do artigo."),
        validators.Length(max=500)
    ])

    keywords = TagsField('keywords',
        choices=[],
        validators=[
            validators.Required(u"Por favor, insira no mínimo uma palavra-chave para o artigo."),
            validate_keywords
        ]
    )

    abstract = HiddenField('abstract', validators=[
        validators.Required(u"Por favor, insira o resumo do artigo."),
        NumberOfWords(max=250)
    ])

    def set_choices(self, keywords_query):
        if self.keywords.data:
            self.keywords.choices = [(name, name) for name in self.keywords.data]
        for keyword in keywords_query:
            if (keyword.name, keyword.name) not in self.keywords.choices:
                self.keywords.choices.append((keyword.name, keyword.name))
