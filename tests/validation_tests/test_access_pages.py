'''
run:  nosetests tests/validation_tests/*py
'''

from flask import g, url_for
from test_base import BaseTestCase


class AccessScreenTests(BaseTestCase):

    def setUp(self):
        g.locale = 'en'

    def test_should_redirect_when_access_root(self):
        assert '302 FOUND' == self.client.get('/').status

    def test_english_home_screen_is_up_and_running(self):
        response = self.client.get('/en/')
        self.assert_200(response)

    def test_portuguese_home_screen_is_up_and_running(self):
        response = self.client.get('/pt/')
        self.assert_200(response)

    def test_home_screen_access(self):
        response = self.client.get('/')
        self.assertRedirects(response, url_for('general.home'))

    def test_about_screen_access(self):
        response = self.client.get(url_for('about.index'))
        self.assert_200(response)

    def test_search_screen_access(self):
        response = self.client.get(url_for('general.search'))
        self.assert_200(response)

    def test_buid_graph_screen_access(self):
        response = self.client.get(url_for('build_graph.index'))
        self.assert_200(response)

    def test_buid_graph_costummer_screen_access(self):
        response = self.client.get(g.locale + 
        	'/build_graph/rais/all/all/all?view=Employment%20by%20Municipality&graph=geo_map')
        self.assert_200(response)

    def test_data_screen_access(self):
        response = self.client.get(url_for('data.index'))
        self.assert_200(response)

    def test_partners_screen_access(self):
        response = self.client.get(url_for('partners.index'))
        self.assert_200(response)

    def test_be_a_partner_screen_access(self):
        response = self.client.get(url_for('partners.be_a_partner'))
        self.assert_200(response)

    def test_help_screen_access(self):
        response = self.client.get(url_for('help.index'))
        self.assert_200(response)

    def test_location_screen_access(self):
        response = self.client.get(g.locale + '/location/4mg')
        self.assert_200(response)

    def test_occupation_screen_access(self):
        response = self.client.get(g.locale + '/occupation/4110')
        self.assert_200(response)

    def test_industry_screen_access(self):
        response = self.client.get(g.locale + '/industry/o84116')
        self.assert_200(response)

    def test_product_screen_access(self):
        response = self.client.get(g.locale + '/product/021201')
        self.assert_200(response)

    def test_trade_partner_screen_access(self):
        response = self.client.get(g.locale + '/trade_partner/aschn')
        self.assert_200(response)

    def test_university_screen_access(self):
        response = self.client.get(g.locale + '/university/00594')
        self.assert_200(response)

    def test_major_screen_access(self):
        response = self.client.get(g.locale + '/major/523E04')
        self.assert_200(response)

    def test_basic_course_screen_access(self):
        response = self.client.get(g.locale + '/basic_course/07085')
        self.assert_200(response)

    def test_scholar_screen_access(self):
        response = self.client.get(url_for('scholar.index'))
        self.assert_200(response)

    def test_scholar_screen_access(self):
        response = self.client.get(url_for('scholar.index'))
        self.assert_200(response)

    def test_news_screen_access(self):
        response = self.client.get(url_for('news.index'))
        self.assert_200(response)

    def test_blog_screen_access(self):
        response = self.client.get(url_for('blog.index'))
        self.assert_200(response)

    def test_contact_screen_access(self):
        response = self.client.get(url_for('contact.index'))
        self.assert_200(response)

    #No test ajax request, only access.
    def test_rankings_index_screen_acces(self):
        response = self.client.get(url_for('rankings.index'))
        self.assert_200(response)

    def test_rankings_location_international_trade_screen_access(self):
        response = self.client.get(url_for('rankings.location_international_trade'))
        self.assert_200(response)

    def test_rankings_location_wages_screen_access(self):
        response = self.client.get(url_for('rankings.location_wages'))
        self.assert_200(response)

    def test_rankings_occupation_screen_access(self):
        response = self.client.get(url_for('rankings.occupation'))
        self.assert_200(response)

    def test_rankings_economic_activities_screen_access(self):
        response = self.client.get(url_for('rankings.economic_activities'))
        self.assert_200(response)

    def test_rankings_product_screen_access(self):
        response = self.client.get(url_for('rankings.product'))
        self.assert_200(response)

    def test_rankings_trade_partner_screen_access(self):
        response = self.client.get(url_for('rankings.trade_partner'))
        self.assert_200(response)

    def test_rankings_university_screen_access(self):
        response = self.client.get(url_for('rankings.university'))
        self.assert_200(response)

    def test_rankings_major_screen_access(self):
        response = self.client.get(url_for('rankings.major'))
        self.assert_200(response)

    def test_rankings_basic_course_screen_access(self):
        response = self.client.get(url_for('rankings.basic_course'))
        self.assert_200(response)
