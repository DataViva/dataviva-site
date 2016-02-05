from dataviva.api.attrs.models import Hs, Stat, Ybs
from dataviva import db
from sqlalchemy import func

class Location:
    def __init__(self, bra_id):
        self._attrs_list = None
        self.bra_id = bra_id
        self.max_year_query = db.session.query(
            func.max(Ybs.year)).filter_by(bra_id=bra_id)
        self.attrs_query = Ybs.query.join(Stat).filter(
            Ybs.bra_id == self.bra_id,
            Ybs.year == self.max_year_query)

    def __attrs_list__(self):
        if not self._attrs_list:
            attrs_data = self.attrs_query.all()
            self._attrs_list = attrs_data
        return self._attrs_list

    def gdp(self):
        statistic_list = self.__attrs_list__()
        return next((s for s in statistic_list if s.id == 'gdp'), None)

class Product:
    def __init__(self, product_id):
        self.product_id = product_id
        self._name = None

    def __product_name__(self):
        if not self._name:
            self._name = Hs.query.filter(Hs.id == self.product_id).first().name()
        return self._name

    def name(self):
        return self.__product_name__()
