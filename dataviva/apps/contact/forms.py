# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, validators, ValidationError


class NumberOfWords(object):
    def __init__(self, max, message=None):
        self.max = max
        if not message:
            message = u"Campo deve possuir no máximo %d palavras." % (max)
        self.message = message

    def __call__(self, form, field):
        if len(field.data.split()) > self.max:
            raise ValidationError(self.message)


class ContactForm(Form):
    name = TextField('name', [validators.Required(u"Por favor, insira o seu nome."), validators.Length(max=100)])
    email = TextField('email', [validators.Required(u"Por favor, insira o seu e-mail."), NumberOfWords(max=1)])
    subject = TextField('subject', [validators.Length(max=200)])
    message = TextAreaField('message', [validators.Required(u"Por favor, insira a mensagem."), NumberOfWords(max=250)])
