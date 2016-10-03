# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SelectMultipleField, validators, ValidationError
from models import KeyWord


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
        validators.Length(max=100)
    ])

    keywords = SelectMultipleField('keywords',
        choices=[(keyword.name, keyword.name) for keyword in KeyWord.query.order_by('name').all()],
        validators=[
            validators.Required(u"Por favor, insira no mínimo uma palavra-chave para o artigo."),
            validate_keywords
        ]
    )

    abstract = TextAreaField('abstract', validators=[
        validators.Required(u"Por favor, insira o resumo do artigo."),
        NumberOfWords(max=250)
    ])

'''
REGRAS FORMULÁRIO:
    Título - (Máximo 400 caracteres)
    Tema - (Máximo 5 palavras)
    Autor - (Exibir FREITAS, E;)
    Palavras-Chave - (Máximo 3 conjuntos)
    Resumo - (Máximo 250 palavras)
    Formato - (PDF, DOC, DOCX - Tamanho máximo de arquivo: 50MB)
'''
