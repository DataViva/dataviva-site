from dataviva.api.attrs.models import Bra
from test_base import BaseTestCase


class AttrModelTests(BaseTestCase):

    def test_minas_gerais_preposition_em_should_be_em(self):
        minas_gerais = Bra.query.filter_by(id='4mg').first()
        assert 'em' == minas_gerais.preposition('em')

    def test_rio_de_janeiro_preposition_em_should_be_no(self):
        rio_de_janeiro = Bra.query.filter_by(id='4rj').first()
        assert 'no' == rio_de_janeiro.preposition('em')
