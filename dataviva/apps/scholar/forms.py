# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import DateField, FileField, TextField, TextAreaField, validators, ValidationError


class RegistrationForm(Form):
    title = TextField('title', [validators.Required(u"Por favor, insira o título do artigo."), validators.Length(max=400)])
    theme = TextField('theme', [validators.Required(u"Por favor, insira o tema do artigo."), validators.Length(max=30)])
    author = TextField('author', [validators.Required(u"Por favor, insira o(s) autor(es) do artigo."), validators.Length(max=30)])
    key_words = TextField('key_words', [validators.Required(u"Por favor, insira as palavras-chave do artigo."), validators.Length(max=30)])
    abstract = TextAreaField('abstract', [validators.Required(u"Por favor, insira o resumo do artigo."), validators.Length(max=30)])
    article_file = FileField('article_file', [validators.Required(u"Por favor, insira o arquivo do artigo.")])


'''
REGRAS FORMULÁRIO:
    Título - (Máximo 400 caracteres)
    Tema - (Máximo 5 palavras)
    Autor - (Exibir FREITAS, E;)
    Palavras-Chave - (Máximo 3 conjuntos)
    Resumo - (Máximo 250 palavras)
    Formato - (PDF, DOC, DOCX - Tamanho máximo de arquivo: 50MB)
'''
