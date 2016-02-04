from dataviva.api.attrs.models import Ybs, Stat, Hs
from dataviva import db
from sqlalchemy import func

class Location:
    def __init__(self, bra_id):

        self._statistics = None

        self.bra_id = bra_id
        self.ybs_max_year_query = db.session.query(
            func.max(Ybs.year)).filter_by(bra_id=bra_id)

    def __statistics__(self):
        if not self._statistics:
            statistics_query = Ybs.query.join(Stat).filter(
                Ybs.bra_id == self.bra_id,
                Ybs.year == self.ybs_max_year_query)

            statistics_data = statistics_query.values(
                Stat.id,
                Stat.name_pt,
                Ybs.stat_val)

            statistics = {}

            for id, name_pt, stat_val in statistics_data:
                statistics[id] = {
                    'name': name_pt,
                    'value': stat_val,
                }

            self._statistics = statistics

        return self._statistics

     def gdp(self):
        return self.__statistics__()['gdp']


class Product:
    def __init__(self, product_id):
        self.product_id = product_id
        self._name = None

    def __product_name__(self):
        if not self._name:
            self._name = Hs.query.filter(Hs.id == self.product_id).first().name()
        return self._name

    def name(self):
        return self.__product_name__()['name']