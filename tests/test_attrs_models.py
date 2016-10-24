'''from dataviva.api.attrs.models import Bra
from test_base import BaseTestCase
from flask import g

class AttrModelTests(BaseTestCase):

    def setUp(self):
        g.locale = 'pt'

    def test_minas_gerais_preposition_em_should_be_em(self):
        minas_gerais = Bra.query.filter_by(id='4mg').first()
        assert 'em' == minas_gerais.preposition('em')

    def test_rio_de_janeiro_preposition_em_should_be_no(self):
        rio_de_janeiro = Bra.query.filter_by(id='4rj').first()
        assert 'no' == rio_de_janeiro.preposition('em')

    def test_paraiba_preposition_em_should_be_na(self):
        paraiba = Bra.query.filter_by(id='2pb').first()
        assert 'na' == paraiba.preposition('em')

    def test_minas_gerais_preposition_de_should_be_de(self):
        minas_gerais = Bra.query.filter_by(id='4mg').first()
        assert 'de' == minas_gerais.preposition('de')

    def test_rio_de_janeiro_preposition_de_should_be_do(self):
        rio_de_janeiro = Bra.query.filter_by(id='4rj').first()
        assert 'do' == rio_de_janeiro.preposition('de')

    def test_paraiba_preposition_de_should_be_da(self):
        paraiba = Bra.query.filter_by(id='2pb').first()
        assert 'da' == paraiba.preposition('de')

    def test_colinas_do_sul_preposition_de_should_be_das(self):
        colinas_do_sul = Bra.query.filter_by(id='3go030003').first()
        assert 'das' == colinas_do_sul.preposition('de')

    def test_sertoes_cearenses_preposition_de_should_be_dos(self):
        sertoes_cearenses = Bra.query.filter_by(id='2ce05').first()
        assert 'dos' == sertoes_cearenses.preposition('de')
'''