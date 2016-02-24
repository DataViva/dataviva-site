from dataviva.api.attrs.models import Ybs
from dataviva import db
from sqlalchemy import func


class Location:
    def __init__(self, bra_id):
        self._attrs_list = None
        self.bra_id = bra_id
        self.max_year_query = db.session.query(
            func.max(Ybs.year)).filter_by(bra_id=bra_id)
        self.attrs_query = Ybs.query.filter(
            Ybs.bra_id == self.bra_id,
            Ybs.year == self.max_year_query)

    def __attrs_list__(self):
        if not self._attrs_list:
            attrs_data = self.attrs_query.all()
            self._attrs_list = attrs_data
        return self._attrs_list

    def gdp(self):
        attrs = self.__attrs_list__()
        attr = next((attr for attr in attrs if attr.stat_id == 'gdp'),
                    None)
        return attr.stat_val

    def life_expectation(self):
        attrs = self.__attrs_list__()
        attr = next((attr for attr in attrs if attr.stat_id == 'life_exp'),
                    None)
        return attr.stat_val

    def population(self):
        attrs = self.__attrs_list__()
        attr = next((attr for attr in attrs if attr.stat_id == 'pop'),
                    None)
        return attr.stat_val

    def gdp_per_capita(self):
        attrs = self.__attrs_list__()
        attr = next((attr for attr in attrs if attr.stat_id == 'gdp_pc'),
                    None)
        return attr.stat_val

    def hdi(self):
        attrs = self.__attrs_list__()
        attr = next((attr for attr in attrs if attr.stat_id == 'hdi'),
                    None)
        return attr.stat_val
