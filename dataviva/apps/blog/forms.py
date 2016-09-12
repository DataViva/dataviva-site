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


def validate_subject_en(form, field):
    if form.dual_language.data:
        if not form.subject_en.data:
            raise ValidationError(u"Por favor, insira a categoria do post.")
        subjects_pt = form.subject_pt.data.replace(', ', ',').split(',')
        subjects_en = form.subject_en.data.replace(', ', ',').split(',')
        if '' in subjects_en:
            raise ValidationError(u"Por favor, insira uma vírgula somente entre duas categorias.")
        if len(subjects_pt) != len(subjects_en):
            raise ValidationError(u"Por favor, insira a mesma quantidade de categorias em português e em inglês.")

def validate_subject_pt(form, field):
    subjects = form.subject_pt.data.replace(', ', ',').split(',')
    if '' in subjects:
        raise ValidationError(u"Por favor, insira uma vírgula somente entre duas categorias.")

class RegistrationForm(Form):
    title_pt = TextField('title_pt', validators=[
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

    subject_pt = TextField('subject_pt', validators=[
        validators.Required(u"Por favor, insira a categoria do post."),
        validate_subject_pt
    ])

    subject_en = TextField('subject_en', validators=[
        validate_subject_en,
    ])

    text_call_pt = TextAreaField('text_call_pt', validators=[
        validators.Required(u"Por favor, insira uma chamada para o post."),
        validators.Length(max=500)
    ])

    text_call_en = TextAreaField('text_call_en', validators=[
        validators.Length(max=500),
        validate_text_call_en
    ])

    text_content_pt = HiddenField('text_content_pt', validators=[
        validators.Required(u"Por favor, insira o conteúdo do post.")
    ]) 

    text_content_en = HiddenField('text_content_en', validators=[
        validate_text_content_en
    ])

    thumb = HiddenField('thumb', validators=[
        validators.Required(u"Por favor, insira uma imagem para a chamada.")
    ])

