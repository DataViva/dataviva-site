from flask.ext.wtf import Form, TextField, TextAreaField, HiddenField
from flask.ext.wtf import Required, Length

class SearchForm(Form):
    search = TextField('search', validators = [Required()])

class AskForm(Form):
    question = TextField('question', validators = [Required()])
    body = TextAreaField('body', validators = [])
    app = TextField('app', validators = [])
    tags = TextField('tags', validators = [])

class ReplyForm(Form):
    reply = TextAreaField('reply', validators = [Required()])
    parent = HiddenField('parent')