# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import DateField, FileField, TextField, TextAreaField, validators, ValidationError
from wtforms_components import DateRange
from datetime import date


class RegistrationForm(Form):
    title = TextField('title', [validators.Required(u"Por favor, insira o título do artigo."), validators.Length(min=4, max=400)])
    theme = TextField('theme', [validators.Required(u"Por favor, insira o tema do artigo."), validators.Length(min=4, max=30)])
    author = TextField('author', [validators.Required(u"Por favor, insira o(s) autor(es) do artigo."), validators.Length(min=4, max=30)])
    key_words = TextField('key_words', [validators.Required(u"Por favor, insira as palavras-chave do artigo."), validators.Length(min=4, max=30)])
    abstract = TextAreaField('abstract', [validators.Required(u"Por favor, insira o resumo do artigo."), validators.Length(min=4, max=30)])
    publication_date = DateField('publication_date', [validators.Required(u"Por favor, insira a data de publicação do artigo."),
                                                     DateRange(min=date(1950, 01, 01), max=date.today())], format='%d/%m/%Y')
    article_file = FileField('article_file', [validators.Required(u"Por favor, insira o arquivo do artigo.")])


'''
REGRAS FORMULÁRIO:
    Título - (Máximo 400 caracteres)
    Tema - (Máximo 5 palavras)
    Autor - (Exibir FREITAS, E;)
    Palavras-Chave - (Máximo 3 conjuntos)
    Resumo - (Máximo 250 palavras)
    Formato - (Somente PDF, Tamanho máximo de arquivo: 50MB)
'''
