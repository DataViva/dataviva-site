from flask.ext.wtf import Form, PasswordField

class AccessForm(Form):
    pw = PasswordField('pw')