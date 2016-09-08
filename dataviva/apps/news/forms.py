# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import HiddenField, TextField, TextAreaField, validators, DateField, BooleanField, ValidationError


def validate_title_en(form, field):
    if form.dual_language.data and not form.title_en.data:
        raise ValidationError(u"Por favor, insira o título da notícia.")


def validate_text_call_en(form, field):
    if form.dual_language.data and not form.text_call_en.data:
        raise ValidationError(u"Por favor, insira a chamada da notícia.")


def validate_text_content_en(form, field):
    if form.dual_language.data and not form.text_content_en.data:
        raise ValidationError(u"Por favor, insira o conteúdo da notícia.")


class RegistrationForm(Form):
    title_pt = TextField('title_pt', validators=[
        validators.Required(u"Por favor, insira o título da notícia."),
        validators.Length(max=400)
    ])

    title_en = TextField('title_en', validators=[
        validators.Length(max=400),
        validate_title_en
    ])

    show_home = BooleanField('show_home')

    dual_language = BooleanField('dual_language')

    author = TextField('author', validators=[
        validators.Required(u"Por favor, insira o autor da notícia."),
        validators.Length(max=100)
    ])

    publish_date = DateField('publish_date', validators=[
        validators.Required(u"Por favor, insira a data da notícia.")],
        format='%d/%m/%Y',
        description='Formato da data: dia/mês/ano'
    )

    subject = TextField('subject', validators=[
        validators.Required(u"Por favor, insira a categoria da notícia.")
    ])

    text_call_pt = TextAreaField('text_call_pt', validators=[
        validators.Required(u"Por favor, insira uma chamada para a notícia."),
        validators.Length(max=500)
    ])

    text_call_en = TextAreaField('text_call_en', validators=[
        validators.Length(max=500),
        validate_text_call_en
    ])

    text_content_pt = HiddenField('text_content_pt', validators=[
        validators.Required(u"Por favor, insira o conteúdo da notícia.")
    ])

    text_content_en = HiddenField('text_content_en', validators=[
        validate_text_content_en
    ])

    thumb = HiddenField('thumb', validators=[
        validators.Required(u"Por favor, insira uma imagem para a chamada.")
    ])
