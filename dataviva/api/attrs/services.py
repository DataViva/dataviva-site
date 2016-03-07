from dataviva.api.attrs.models import Ybs, Bra, Bs, Yb
from dataviva import db
from sqlalchemy import func


class Location:

    def __init__(self, bra_id):
        self._attrs_list = None
        self._ybs_sorted_by_ranking = None
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

    def __ybs_sorted_by_ranking__(self):
        if not self._ybs_sorted_by_ranking:
            self._ybs_sorted_by_ranking = self.__attrs_list__()
            self._ybs_sorted_by_ranking.sort(
                key=lambda ybs: ybs.stat_val, reverse=True)
        return self._ybs_sorted_by_ranking

    def ranking(self):
        ranking_list = self.__ybs_sorted_by_ranking__()
        rank = 1
        for ranking in ranking_list:
            if ranking.bra_id == self.bra_id:
                return rank
                break
            rank += 1

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

    def area(self):
        bs_query = Bs.query.filter(Bra.id == self.bra_id).first()
        return bs_query.stat_val


class LocationGdpRankings(Location):

    def __init__(self, bra_id, stat_id):
        Location.__init__(self, bra_id)
        self.stat_id = stat_id
        self.attrs_query = Ybs.query.filter(
            Ybs.stat_id == self.stat_id,
            Ybs.bra_id.like(self.bra_id[:3]+'%'),
            Ybs.year == self.max_year_query,
            func.length(Ybs.bra_id) == len(self.bra_id))

    def gdp_rank(self):
        gdp_position = self.ranking()
        return gdp_position


class LocationGdpPerCapitaRankings(Location):

    def __init__(self, bra_id):
        Location.__init__(self, bra_id)
        self.attrs_query = Ybs.query.filter(
            Ybs.stat_id == 'gdp_pc',
            Ybs.year == self.max_year_query,
            func.length(Ybs.bra_id) == len(self.bra_id))

    def gdp_pc_rank(self):
        gdp_pc_position = self.ranking()
        return gdp_pc_position


class LocationPopRankings(Location):

    def __init__(self, bra_id):
        Location.__init__(self, bra_id)
        self.attrs_query = Yb.query.filter(
            Ybs.year == self.max_year_query,
            func.length(Ybs.bra_id) == len(self.bra_id))

    def pop_rank(self):
        pop = self.attrs_query.all()
        pop_position = 1
        for r in pop:
            if r.bra_id == self.bra_id:
                return pop_position
            pop_position += 1
