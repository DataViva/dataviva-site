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
    title = TextField('title', [validators.Required(u"Por favor, insira o título do artigo."), validators.Length(max=400)])
    theme = TextField('theme', [validators.Required(u"Por favor, insira o tema do artigo."), NumberOfWords(max=5)])
    author = TextField('author', [validators.Required(u"Por favor, insira o(s) autor(es) do artigo."), validators.Length(max=50)])
    key_words = TextField('key_words', [validators.Required(u"Por favor, insira as palavras-chave do artigo."), NumberOfWords(max=3)])
    abstract = TextAreaField('abstract', [validators.Required(u"Por favor, insira o resumo do artigo."), NumberOfWords(max=250)])
    article_file = FileField('article_file', [validators.Required(u"Por favor, insira o arquivo do artigo.")])


'''
REGRAS FORMULÁRIO:
    Título - (Máximo 400 caracteres) >>> OK
    Tema - (Máximo 5 palavras) >>> OK
    Autor - (Exibir FREITAS, E;) >>> NO
    Palavras-Chave - (Máximo 3 conjuntos) >>> OK
    Resumo - (Máximo 250 palavras) >>> OK
    Formato - (PDF, DOC, DOCX - Tamanho máximo de arquivo: 50MB) >>> Definir Regra
'''
