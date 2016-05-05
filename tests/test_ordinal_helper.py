# -​*- coding: utf-8 -*​-
from dataviva.utils.jinja_helpers import ordinal
from flask import g
from test_base import BaseTestCase


class OrdinalENTests(BaseTestCase):

    def setUp(self):
        g.locale = 'en'

    def test_ordinal_1_should_be_st(self):
        assert 'st' == ordinal(1)

    def test_ordinal_2_should_be_nd(self):
        assert 'nd' == ordinal(2)

    def test_ordinal_3_should_be_rd(self):
        assert 'rd' == ordinal(3)

    def test_ordinal_4_should_be_th(self):
        assert 'th' == ordinal(4)

    def test_ordinal_5_should_be_th(self):
        assert 'th' == ordinal(5)

    def test_ordinal_6_should_be_th(self):
        assert 'th' == ordinal(6)

    def test_ordinal_7_should_be_th(self):
        assert 'th' == ordinal(7)

    def test_ordinal_8_should_be_th(self):
        assert 'th' == ordinal(8)

    def test_ordinal_9_should_be_th(self):
        assert 'th' == ordinal(9)

    def test_ordinal_0_should_be_th(self):
        assert 'th' == ordinal(0)

    def test_ordinal_31_should_be_st(self):
        assert 'st' == ordinal(31)

    def test_ordinal_1000000_should_be_th(self):
        assert 'th' == ordinal(1000000)


class OrdinalPTTests(BaseTestCase):

    def setUp(self):
        g.locale = 'pt'

    def test_ordinal_male_1_should_be_o(self):
        assert 'º' == ordinal(1, gender='m')

    def test_ordinal_male_2_should_be_o(self):
        assert 'º' == ordinal(2, gender='m')

    def test_ordinal_male_3_should_be_o(self):
        assert 'º' == ordinal(3, gender='m')

    def test_ordinal_male_4_should_be_o(self):
        assert 'º' == ordinal(4, gender='m')

    def test_ordinal_male_5_should_be_o(self):
        assert 'º' == ordinal(5, gender='m')

    def test_ordinal_male_6_should_be_o(self):
        assert 'º' == ordinal(6, gender='m')

    def test_ordinal_male_7_should_be_o(self):
        assert 'º' == ordinal(7, gender='m')

    def test_ordinal_male_8_should_be_o(self):
        assert 'º' == ordinal(8, gender='m')

    def test_ordinal_male_9_should_be_o(self):
        assert 'º' == ordinal(9, gender='m')

    def test_ordinal_male_0_should_be_o(self):
        assert 'º' == ordinal(0, gender='m')

    def test_ordinal_female_0_should_be_a(self):
        assert 'ª' == ordinal(0, gender='f')

    def test_ordinal_female_1_should_be_a(self):
    	assert 'ª' == ordinal(1, gender='f')

    def test_ordinal_female_2_should_be_a(self):
        assert 'ª' == ordinal(2, gender='f')

    def test_ordinal_female_3_should_be_a(self):
        assert 'ª' == ordinal(3, gender='f')

    def test_ordinal_female_4_should_be_a(self):
        assert 'ª' == ordinal(4, gender='f')

    def test_ordinal_female_5_should_be_a(self):
        assert 'ª' == ordinal(5, gender='f')

    def test_ordinal_female_6_should_be_a(self):
        assert 'ª' == ordinal(6, gender='f')

    def test_ordinal_female_7_should_be_a(self):
        assert 'ª' == ordinal(7, gender='f')

    def test_ordinal_female_8_should_be_a(self):
        assert 'ª' == ordinal(8, gender='f')

    def test_ordinal_female_9_should_be_a(self):
        assert 'ª' == ordinal(9, gender='f')
