from dataviva.utils.jinja_helpers import ordinal
from flask import g
from test_base import BaseTestCase


class OrdinalENTests(BaseTestCase):

    def setUp(self):
        g.locale = 'pt'

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
