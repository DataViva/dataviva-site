from flask.ext.wtf import Form, TextField, TextAreaField, BooleanField, QuerySelectField, HiddenField
from flask.ext.wtf import Required, Length, url

def statuses():
    return Status.query.all()
    
class StatusForm(Form):
    status = QuerySelectField(query_factory=statuses)

class StatusNotesForm(Form):
    status_notes = TextAreaField('status_notes', validators = [])