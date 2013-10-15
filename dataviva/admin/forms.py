from flask.ext.wtf import Form, TextField, TextAreaField, BooleanField, QuerySelectField, SelectField, HiddenField
from flask.ext.wtf import Required, Length, url
from dataviva.ask.models import Status, Question
from sqlalchemy import distinct

def statuses():
    return Status.query.all()

class AdminQuestionUpdateForm(Form):
    previous_status = HiddenField('previous_status')
    status = QuerySelectField(query_factory=statuses)
    language = SelectField("language",choices=[("en","English"),("pt","Portugu&#234;s")])
    answer = TextAreaField('answer', validators = [Required()])