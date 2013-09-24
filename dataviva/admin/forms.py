from flask.ext.wtf import Form, TextField, TextAreaField, BooleanField, QuerySelectField, HiddenField
from flask.ext.wtf import Required, Length, url
from dataviva.ask.models import Status

def statuses():
    return Status.query.all()

class AdminQuestionUpdateForm(Form):
    previous_status = HiddenField('previous_status')
    status = QuerySelectField(query_factory=statuses)
    answer = TextAreaField('answer', validators = [Required()])