from flask import g, url_for
from test_base import BaseTestCase
from dataviva.apps.session.forms import LoginForm

class UserTests(BaseTestCase):

    def setUp(self):
        g.locale = 'en'


	def login(self, email, password):
		form = LoginForm();
		form.email.data = email
		form.email.password.data = password
	  	return self.client.post('/' + g.locale + '/session/login', form=form, follow_redirects=True)

	def logout(self):
	    return self.client.get('/' + g.locale + 'session/logout', follow_redirects=True)

    def test_login(self):
		data=dict(email='gilmardealcantara@gmail.com', password='123456')
	  	rv = self.client.post('/en/session/login?html_form=test', data=data, follow_redirects=True)
		assert 'You were logged in' in rv.data


'''
from flask.ext.login import login_user, logout_user, current_user
app.config['WTF_CSRF_ENABLED'] = False
app.testing=True
data=dict(email='gilmardealcantara@gmail.com', password='123456')
response = app.test_client().post('/en/session/login', data=data, follow_redirects=True)
'''
