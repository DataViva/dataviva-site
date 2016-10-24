'''from flask import url_for
from test_base import BaseTestCase


class GeneralModuleTests(BaseTestCase):

    def test_should_redirect_when_access_root(self):
        assert '302 FOUND' == self.client.get('/').status

    def test_should_redirect_to_home_screen(self):
        response = self.client.get('/')
        self.assertRedirects(response, url_for('general.home'))

    def test_english_home_screen_is_up_and_running(self):
        response = self.client.get('/en/')
        self.assert_200(response)

    def test_portuguese_home_screen_is_up_and_running(self):
        response = self.client.get('/pt/')
        self.assert_200(response)
'''