from dataviva.api.attrs.models import Ybs, Bra
from dataviva import db
from sqlalchemy import func


class Location:

    def __init__(self, bra_id):
        self._attrs_list = None
        self.bra_id = bra_id
        if len(bra_id) != 9 and len(bra_id) != 3:
            like_cond = bra_id[:len(bra_id)]+'%'
            self.max_year_query = db.session.query(
                func.max(Ybs.year)).filter(Ybs.bra_id.like(like_cond))
            self.attrs_query = db.session.query(func.sum(Ybs.stat_val).label("stat_val"), Ybs.stat_id).filter(
                Ybs.bra_id.like(like_cond),
                func.length(Ybs.bra_id) == 9,
                Ybs.year == self.max_year_query).group_by(Ybs.stat_id)
        else:
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

    def hdi(self):
        attrs = self.__attrs_list__()
        attr = next((attr for attr in attrs if attr.stat_id == 'hdi'),
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

    def name(self):
        bra_query = Bra.query.filter(Bra.id == self.bra_id).first()
        return bra_query.name()

    def number_of_locations(self, bra_length):
        if bra_length == 1 or bra_length == 3:
            bra_query = db.session.query(func.count(Bra.id).label("total")).filter(
                func.length(Bra.id) == bra_length)
        elif bra_length == 7:
            bra_query = db.session.query(func.count(Bra.id).label("total")).filter(
                Bra.id.like(self.bra_id[:5]+'%'),
                func.length(Bra.id) == bra_length)
        else:
            bra_query = db.session.query(func.count(Bra.id).label("total")).filter(
                Bra.id.like(self.bra_id[:3]+'%'),
                func.length(Bra.id) == bra_length)
        bra = bra_query.first()
        return bra.total

    def location_name(self, bra_length):
        bra_query = Bra.query.filter(
            Bra.id == self.bra_id[:bra_length]).first()
        return bra_query.name()

    def number_of_municipalities(self):
        bra_query = db.session.query(func.count(Bra.id).label("total")).filter(
                Bra.id.like(self.bra_id[:7]+'%'),
                func.length(Bra.id) == 9)
        bra = bra_query.one()
        return bra.total