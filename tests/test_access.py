from flask import g, url_for
from test_base import BaseTestCase


class GeneralModuleTests(BaseTestCase):


    def setUp(self):
        g.locale = 'en'

    def test_should_redirect_when_access_root(self):
        assert '302 FOUND' == self.client.get('/').status

#    def test_english_home_screen_is_up_and_running(self):
#        response = self.client.get('/en/')
#        self.assert_200(response, message=None)

#    def test_portuguese_home_screen_is_up_and_running(self):
#        response = self.client.get('/pt/')
#        self.assert_200(response)

    def test_should_redirect_to_home_screen(self):
        response = self.client.get('/')
        self.assertRedirects(response, url_for('general.home'))

    def test_should_redirect_to_help_screen(self):
        response = self.client.get(url_for('help.index'))
        self.assert_200(response)

    def test_should_redirect_to_search_screen(self):
        response = self.client.get(url_for('general.search'))
        self.assert_200(response)

    def test_should_redirect_to_rankings_screen(self):
        response = self.client.get(url_for('rankings.index'))
        self.assert_200(response)

