from dataviva.api.attrs.models import Ybs, Bra, Bs, Yb
from dataviva import db
from sqlalchemy import func


class All:

    def __init__(self):

        self.max_coincident_year = db.session.query(func.max(Ybs.year)) \
            .filter(Ybs.stat_id.in_(["gdp", "pop"])) \
            .group_by(Ybs.year) \
            .having(func.count(func.distinct(Ybs.stat_id)) == 2) \
            .order_by(Ybs.year.desc()) \
            .limit(1).first()[0]

        self.attrs_query_ybs_gdp = db.session.query(func.sum(Ybs.stat_val).label("stat_val")).filter(
            func.length(Ybs.bra_id) == 1,
            Ybs.stat_id == "gdp")

        self.attrs_query_ybs_pop = db.session.query(func.sum(Ybs.stat_val).label("stat_val")).filter(
            func.length(Ybs.bra_id) == 1,
            Ybs.stat_id == "pop")

    def year_gdp(self):
        max_year_query_ybs_gdp = db.session.query(func.max(Ybs.year)) \
            .filter(Ybs.stat_id == "gdp") \
            .filter(func.length(Ybs.bra_id) == 1).first()[0]
        return max_year_query_ybs_gdp

    def year_pop(self):
        max_year_query_ybs_pop = db.session.query(func.max(Ybs.year)) \
            .filter(Ybs.stat_id == "pop") \
            .filter(func.length(Ybs.bra_id) == 1).first()[0]
        return max_year_query_ybs_pop

    def gdp(self, year=""):
        if(year==""):
            year=self.year_gdp()

        gdp = self.attrs_query_ybs_gdp.filter(
            Ybs.year == year).first()[0]
        return gdp

    def population(self, year=""):
        if(year==""):
            year=self.year_pop()
        population = self.attrs_query_ybs_pop.filter(
            Ybs.year == year).first()[0]
        return population

    def gdp_per_capita(self):
        gdp_per_capita = self.gdp(self.max_coincident_year) / self.population(self.max_coincident_year)
        return gdp_per_capita


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
                Ybs.bra_id == self.bra_id)

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

    def __attrs__max__year__(self, stat_id):
        max_year = db.session.query(
            func.max(Ybs.year)).filter_by(stat_id=stat_id, bra_id=self.bra_id).all()[0][0]
        return max_year

    def gdp_year(self):
        return self.__attrs__max__year__('gdp')

    def hdi_year(self):
        return self.__attrs__max__year__('hdi')

    def life_expectation_year(self):
        return self.__attrs__max__year__('life_exp')

    def population_year(self):
        return self.__attrs__max__year__('pop')

    def gdp_per_capita_year(self):
        return self.__attrs__max__year__('gdp_pc')

    def gdp(self):
        attrs = self.__attrs_list__()
        if len(self.bra_id) != 9 and len(self.bra_id) != 3:
            attr = next((attr for attr in attrs if (attr.stat_id == 'gdp')),
                        None)
        else:
            attr = next((attr for attr in attrs if (attr.stat_id == 'gdp' and attr.year == self.gdp_year())),
                        None)
        if (getattr(attr, 'stat_val', None)):
            return attr.stat_val

        return attr

    def hdi(self):
        attrs = self.__attrs_list__()
        if len(self.bra_id) != 9 and len(self.bra_id) != 3:
            attr = next((attr for attr in attrs if (attr.stat_id == 'hdi')),
                        None)
        else:
            attr = next((attr for attr in attrs if (attr.stat_id == 'hdi' and attr.year == self.hdi_year())),
                        None)
        if (getattr(attr, 'stat_val', None)):
            return attr.stat_val

        return attr

    def life_expectation(self):
        attrs = self.__attrs_list__()
        if len(self.bra_id) != 9 and len(self.bra_id) != 3:
            attr = next((attr for attr in attrs if (attr.stat_id == 'life_exp')),
                        None)
        else:
            attr = next((attr for attr in attrs if (attr.stat_id == 'life_exp' and attr.year == self.life_expectation_year())),
                        None)
        if (getattr(attr, 'stat_val', None)):
            return attr.stat_val

        return attr

    def population(self):
        attrs = self.__attrs_list__()
        if len(self.bra_id) != 9 and len(self.bra_id) != 3:
            attr = next((attr for attr in attrs if (attr.stat_id == 'pop')),
                        None)
        else:
            attr = next((attr for attr in attrs if (attr.stat_id == 'pop' and attr.year == self.population_year())),
                        None)
        if (getattr(attr, 'stat_val', None)):
            return attr.stat_val

        return attr

    def gdp_per_capita(self):
        attrs = self.__attrs_list__()
        if len(self.bra_id) != 9 and len(self.bra_id) != 3:
            attr = next((attr for attr in attrs if (attr.stat_id == 'gdp_pc')),
                        None)
        else:
            attr = next((attr for attr in attrs if (attr.stat_id == 'gdp_pc' and attr.year == self.gdp_per_capita_year())),
                        None)
        if (getattr(attr, 'stat_val', None)):
            return attr.stat_val

        return attr

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
        bs_query = Bs.query.filter(
            Bs.bra_id == self.bra_id, Bs.stat_id == 'area').first()
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
