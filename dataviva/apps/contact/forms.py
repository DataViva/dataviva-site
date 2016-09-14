# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, validators


class ContactForm(Form):
    name = TextField('name', validators=[validators.Required(message="form_contact_name"), validators.Length(max=50)])
    email = TextField('email', validators=[validators.Required(message="form_contact_email_required"), validators.Email(message="form_contact_email")])
    subject = TextField('subject', validators=[validators.Required(message="form_contact_subject"), validators.Length(max=50)])
    message = TextAreaField('message', validators=[validators.Required(message="form_contact_message"), validators.Length(max=500)])
