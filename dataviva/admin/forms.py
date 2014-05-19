from flask_wtf import Form
from wtforms import TextField, TextAreaField, BooleanField, SelectField, HiddenField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from dataviva.ask.models import Status, Question
from sqlalchemy import distinct

def statuses():
    return Status.query.all()

class AdminQuestionUpdateForm(Form):
    previous_status = HiddenField('previous_status')
    status = QuerySelectField(query_factory=statuses)
    language = SelectField("language",choices=[("en","English"),("pt","Portugu&#234;s")])
    answer = TextAreaField('answer', validators = [validators.Required()])
    body = TextAreaField('body', validators = [validators.Required()])
    question = TextField("question", validators = [validators.Required()])