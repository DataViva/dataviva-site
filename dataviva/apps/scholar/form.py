# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, validators, ValidationError


class RegistrationForm(Form):
    title = TextField('title', [validators.Length(min=4, max=30), validators.Required(u"Por favor, insira o título do artigo.")])
    theme = TextField('theme', [validators.Length(min=4, max=30), validators.Required(u"Por favor, insira o tema do artigo.")])
    author = TextField('author', [validators.Length(min=4, max=30), validators.Required(u"Por favor, insira o(s) autor(es) do artigo.")])
    key_words = TextField('key_words', [validators.Length(min=4, max=30), validators.Required(u"Por favor, insira as palavras-chave do artigo.")])
    abstract = TextField('abstract', [validators.Length(min=4, max=30), validators.Required(u"Por favor, insira o resumo do artigo.")])
    publication_date = TextField('publication_date', [validators.Length(min=4, max=30), validators.Required(u"Por favor, insira a data de publicação do artigo.")])
