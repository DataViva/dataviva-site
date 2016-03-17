# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField,validators

class RegistrationForm(Form):
    title = TextField('title', [validators.Required(u"Por favor, insira o título da chamada."), validators.Length(max=400)])
    link = TextField('link', [validators.Required(u"Por favor, insira o link da chamada.")])