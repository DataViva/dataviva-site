from flask import g, url_for
from test_base import BaseTestCase
from dataviva import test_user_email, test_user_password

class UserTests(BaseTestCase):

    def setUp(self):
        g.locale = 'en'

    def test_users_can_login_and_logout(self):
		data=dict(email=test_user_email, password=test_user_password)
	  	response = self.client.post('/en/session/login', data=data)
	  	assert '302 FOUND' == response.status
	  	response = self.client.get('/logout')
	  	assert '302 FOUND' == response.status