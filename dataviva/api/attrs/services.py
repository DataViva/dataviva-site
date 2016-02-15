from dataviva.api.attrs.models import Ybs, Stat
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
        attrs = self.__attrs_list__()
        return next((attr for attr in attrs if attr.stat_id == 'gdp'), None)
