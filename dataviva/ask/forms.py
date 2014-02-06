from flask_wtf import Form
from wtforms import TextField, TextAreaField, HiddenField,RadioField, validators

class SearchForm(Form):
    search = TextField('search', validators = [validators.Required()])

class AskForm(Form):
    question = TextField('question', validators = [validators.Required()])
    body = TextAreaField('body', validators = [])
    app = TextField('app', validators = [])
    tags = TextField('tags', validators = [])
    type = RadioField(u'Type', choices=[
        ('1', u'Question'),
        ('2', u'Comment'),('3', u'Contact')],
        default=2, validators=[validators.Required()])

class ReplyForm(Form):
    reply = TextAreaField('reply', validators = [validators.Required()])
    parent = HiddenField('parent')