from flask import g, url_for
from test_base import BaseTestCase


class UserTests(BaseTestCase):

    def setUp(self):
        g.locale = 'en'

    def test_users_can_login_and_logout(self):
		data=dict(email='gilmardealcantara@gmail.com', password='123456')
	  	response = self.client.post('/en/session/login', data=data)
	  	assert '302 FOUND' == response.status
	  	responde = self.client.get('/logout')
	  	assert '302 FOUND' == response.status
