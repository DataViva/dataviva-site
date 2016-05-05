from dataviva.api.attrs.models import Ybs, Bra, Bs, Yb
from dataviva import db
from sqlalchemy import func


class All:

    def __init__(self):
        self._attrs_list_ybs = None
        self._attrs_list_yb = None

        self.max_year_query_ybs = db.session.query(
            func.max(Ybs.year))

        self.attrs_query_ybs = db.session.query(func.sum(Ybs.stat_val).label("stat_val"), Ybs.stat_id).filter(
            func.length(Ybs.bra_id) == 1,
            Ybs.year == self.max_year_query_ybs).group_by(Ybs.stat_id)

        self.max_year_query_yb = db.session.query(
            func.max(Yb.year))

        self.attrs_query_yb = db.session.query(func.sum(Yb.population).label("population")).filter(
            func.length(Yb.bra_id) == 1,
            Yb.year == self.max_year_query_yb)

    def __attrs_list_ybs__(self):
        if not self._attrs_list_ybs:
            attrs_data_ybs = self.attrs_query_ybs.first()
            self._attrs_list_ybs = attrs_data_ybs
        return self._attrs_list_ybs

    def gdp(self):
        gdp = self.__attrs_list_ybs__()[0]
        return gdp

    def __attrs_list_yb__(self):
        if not self._attrs_list_yb:
            attrs_data_yb = self.attrs_query_yb.first()
            self._attrs_list_yb = attrs_data_yb
        return self._attrs_list_yb

    def population(self):
        population = self.__attrs_list_yb__()[0]
        return population

    def gdp_per_capita(self):
        gdp_per_capita = self.gdp() / float(self.population())
        return gdp_per_capita

    def year_yb(self):
        year_yb = self.max_year_query_yb.first()[0]
        return year_yb

    def year_ybs(self):
        year_ybs = self.max_year_query_ybs.first()[0]
        return year_ybs


class Location:

    def __init__(self, bra_id):
        self._attrs_list = None
        self._ybs_sorted_by_ranking = None
        self.bra_id = bra_id
        if len(bra_id) != 9 and len(bra_id) != 3:
            like_cond = bra_id[:len(bra_id)] + '%'
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

    def year(self):
        return self.max_year_query.first()[0]

    def number_of_locations(self, bra_length):
        if bra_length == 1 or bra_length == 3:
            bra_query = db.session.query(func.count(Bra.id).label("total")).filter(
                func.length(Bra.id) == bra_length)
        elif bra_length == 7:
            bra_query = db.session.query(func.count(Bra.id).label("total")).filter(
                Bra.id.like(self.bra_id[:5] + '%'),
                func.length(Bra.id) == bra_length)
        else:

            bra_query = db.session.query(func.count(Bra.id).label("total")).filter(
                Bra.id.like(self.bra_id[:3] + '%'),
                func.length(Bra.id) == bra_length)

        bra = bra_query.first()
        return bra.total

    def location_name(self, bra_length):
        bra_query = Bra.query.filter(
            Bra.id == self.bra_id[:bra_length]).first()
        return bra_query.name()

    def number_of_municipalities(self):
        bra_query = db.session.query(func.count(Bra.id).label("total")).filter(
            Bra.id.like(self.bra_id[:7] + '%'),
            func.length(Bra.id) == 9)
        bra = bra_query.one()
        return bra.total

    def area(self):
        bs_query = Bs.query.filter(Bra.id == self.bra_id).first()
        return bs_query.stat_val

    def states_in_a_region(self):
        bra_query = Bra.query.filter(Bra.id.like(self.bra_id + '%'),
                                     func.length(Bra.id) == 3)
        bra = bra_query.all()
        states = []
        for b in bra:
            states.append(b.name())
        return states

    def neighbors(self):
        bs_query = Bs.query.filter(Bs.bra_id == self.bra_id,
                                   Bs.stat_id == 'neighbors')
        bs = bs_query.one()
        neighbors_cod = bs.stat_val.split(',')
        neighbors_name = []
        for neighbor in neighbors_cod:
            bra_query = Bra.query.filter(Bra.id == neighbor)
            bra = bra_query.one()
            neighbors_name.append(bra.name())
        return neighbors_name


class LocationGdpRankings(Location):

    def __init__(self, bra_id, stat_id):
        Location.__init__(self, bra_id)
        self.stat_id = stat_id
        self.attrs_query = Ybs.query.filter(
            Ybs.stat_id == self.stat_id,
            Ybs.bra_id.like(self.bra_id[:3] + '%'),
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
        self.max_year_query = db.session.query(
            func.max(Yb.year)).filter(Yb.bra_id == bra_id)
        self.attrs_query = Yb.query.filter(
            Yb.year == self.max_year_query,
            func.length(Yb.bra_id) == len(self.bra_id))

    def pop_rank(self):
        pop = self.__attrs_list__()
        pop.sort(key=lambda pop: pop.population, reverse=True)
        pop_position = 1
        for r in pop:
            if r.bra_id == self.bra_id:
                return pop_position
            pop_position += 1


class LocationAreaRankings(Location):

    def __init__(self, bra_id):
        Location.__init__(self, bra_id)
        self.attrs_query = Bs.query.filter(
            Bs.stat_id == 'area',
            func.length(Bs.bra_id) == len(self.bra_id))

    def area_rank(self):
        area_position = self.ranking()
        return area_position


class LocationMunicipalityRankings(Location):

    def __init__(self, bra_id):
        Location.__init__(self, bra_id)
        self.attrs_query = db.session.query(func.count(Bra.id).label('count'),
                                            func.left(Bra.id, 3).label('state'))\
            .filter(func.length(Bra.id) == 9).group_by(func.left(Bra.id, 3))

    def municipality_rank(self):
        mun = self.__attrs_list__()
        mun.sort(key=lambda mun: mun.count, reverse=True)
        mun_position = 1
        for r in mun:
            if r.state == self.bra_id:
                if r.state == '3df':
                    return mun_position - 1
                return mun_position
            mun_position += 1
