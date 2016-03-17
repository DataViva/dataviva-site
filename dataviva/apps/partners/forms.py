# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import FileField, TextField, TextAreaField, validators, ValidationError

class RegistrationForm(Form):
    title = TextField('title', [validators.Required(u"Por favor, insira o título do artigo."), validators.Length(max=400)])
    link = TextField('link', [validators.Required(u"Por favor, insira o tema do artigo.")])
   

'''
REGRAS FORMULÁRIO:
    Título - (Máximo 400 caracteres) >>> OK
    Tema - (Máximo 5 palavras) >>> OK
    Autor - (Exibir FREITAS, E;) >>> NO
    Palavras-Chave - (Máximo 3 conjuntos) >>> OK
    Resumo - (Máximo 250 palavras) >>> OK
    Formato - (PDF, DOC, DOCX - Tamanho máximo de arquivo: 50MB) >>> Definir Regra
'''
