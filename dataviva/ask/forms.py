from flask_wtf import Form
from wtforms import TextField, TextAreaField, HiddenField, validators

class SearchForm(Form):
    search = TextField('search', validators = [validators.Required()])

class AskForm(Form):
    question = TextField('question', validators = [validators.Required()])
    body = TextAreaField('body', validators = [])
    app = TextField('app', validators = [])
    tags = TextField('tags', validators = [])

class ReplyForm(Form):
    reply = TextAreaField('reply', validators = [validators.Required()])
    parent = HiddenField('parent')