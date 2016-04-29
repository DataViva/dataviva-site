from flask_wtf import Form
from wtforms import TextField, TextAreaField, HiddenField,RadioField, validators
from flask.ext.babel import lazy_gettext

class SearchForm(Form):
    search = TextField('search', validators = [validators.Required()])

class AskForm(Form):
    question = TextField('question', validators = [validators.Required()])
    body = TextAreaField('body', validators = [])
    app = TextField('app', validators = [])
    tags = TextField('tags', validators = [])
    type = RadioField(u'Type', choices=[
        ('1', lazy_gettext('Question')),
        ('2', lazy_gettext('Comment')),('3', lazy_gettext('Contact'))],
        default=2, validators=[validators.Required()])

class ReplyForm(Form):
    reply = TextAreaField('reply', validators = [validators.Required()])
    parent = HiddenField('parent')