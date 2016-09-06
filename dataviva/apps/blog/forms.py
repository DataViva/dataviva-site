# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import HiddenField, TextField, TextAreaField, DateField, BooleanField, validators, ValidationError


def validate_title_en(form, field):
    if form.dual_language.data and not form.title_en.data:
        raise ValidationError(u"Por favor, insira o título do post.")


def validate_text_call_en(form, field):
    if form.dual_language.data and not form.text_call_en.data:
        raise ValidationError(u"Por favor, insira a chamada do post.")


def validate_text_content_en(form, field):
    if form.dual_language.data and not form.text_content_en.data:
        raise ValidationError(u"Por favor, insira o conteúdo do post.")


class RegistrationForm(Form):
    title = TextField('title', validators=[
        validators.Required(u"Por favor, insira o título do post."),
        validators.Length(max=400)
    ])

    title_en = TextField('title_en', validators=[
        validators.Length(max=400),
        validate_title_en
    ])

    show_home = BooleanField('show_home')

    dual_language = BooleanField('dual_language')

    author = TextField('author', validators=[
        validators.Required(u"Por favor, insira o autor do post."),
        validators.Length(max=100)
    ])

    publish_date = DateField('publish_date', validators=[
        validators.Required(u"Por favor, insira a data do post.")],
        format='%d/%m/%Y',
        description='Formato da data: dia/mês/ano'
    )

    subject = TextField('subject', validators=[
        validators.Required(u"Por favor, insira a categoria do post.")
    ])

    text_call = TextAreaField('text_call', validators=[
        validators.Required(u"Por favor, insira uma chamada para o post."),
        validators.Length(max=500)
    ])

    text_call_en = TextAreaField('text_call_en', validators=[
        validators.Length(max=500),
        validate_text_call_en
    ])

    text_content = HiddenField('text_content', validators=[
        validators.Required(u"Por favor, insira o conteúdo do post.")
    ]) 

    text_content_en = HiddenField('text_content_en', validators=[
        validate_text_content_en
    ])

    thumb = HiddenField('thumb', validators=[
        validators.Required(u"Por favor, insira uma imagem para a chamada.")
    ])

