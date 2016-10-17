# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import SelectField, HiddenField, TextField, TextAreaField, validators, DateField, BooleanField, ValidationError
from dataviva.utils.custom_fields import TagsField
from models import PublicationSubject


class RegistrationForm(Form):
    title_pt = TextField('title_pt', validators=[
        validators.Required(u"Por favor, insira o título da notícia."),
        validators.Length(max=400)
    ])

    show_home = BooleanField('show_home')

    author = TextField('author', validators=[
        validators.Required(u"Por favor, insira o autor da notícia."),
        validators.Length(max=100)
    ])

    publish_date = DateField('publish_date', validators=[
        validators.Required(u"Por favor, insira a data da notícia.")],
        format='%d/%m/%Y',
        description='Formato da data: dia/mês/ano'
    )

    subject_pt = TagsField('subject_pt',
        choices=[],
        validators=[
            validators.Required(u"Por favor, insira a categoria do post."),
    ])

    text_call_pt = TextAreaField('text_call_pt', validators=[
        validators.Required(u"Por favor, insira uma chamada para a notícia."),
        validators.Length(max=500)
    ])

    text_content_pt = HiddenField('text_content_pt', validators=[
        validators.Required(u"Por favor, insira o conteúdo da notícia.")
    ])

    thumb = HiddenField('thumb', validators=[
        validators.Required(u"Por favor, insira uma imagem para a chamada.")
    ])

    language = SelectField('language',
        choices=[('pt', 'Português'), ('en', 'Inglês')],
    )

    def set_remaining_choices(self):
        subject_pt_query = PublicationSubject.query.filter_by(
            language='pt').order_by(PublicationSubject.name)
        self.subject_pt.choices.extend([(subject.name, subject.name) for subject in subject_pt_query if (
            subject.name, subject.name) not in self.subject_pt.choices])
