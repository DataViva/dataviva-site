from dataviva.utils.jinja_helpers import ordinal
from test_base import BaseTestCase


class OrdinalTests(BaseTestCase):

    def test_ordinal_1_should_be_st(self):
        assert 'st' == ordinal(1)
