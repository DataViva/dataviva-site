from dataviva.api.attrs.models import Bra, Hs, Wld
from dataviva.api.secex.models import Ymw, Ymbw, Ympw, Ymp, Ymbp, Ymbpw, Ymb
from dataviva import db
from sqlalchemy.sql.expression import func


class TradePartner:

    def __init__(self, wld_id, bra_id):
        self._secex = None
        self._secex_sorted_by_balance = None
        self._secex_sorted_by_exports = None
        self._secex_sorted_by_imports = None
        self.wld_id = wld_id
        self.bra_id = bra_id
        self.max_database_year = db.session.query(func.max(Ymw.year))
        self.max_year_query = db.session.query(
            func.max(Ymw.year)).filter_by(wld_id=wld_id).filter(
            Ymw.year < self.max_database_year)
        if bra_id is not None:
            self.secex_query = Ymbw.query.join(Wld).filter(
                Ymbw.wld_id == self.wld_id,
                Ymbw.bra_id == self.bra_id,
                Ymbw.month == 0,
                Ymbw.year == self.max_year_query)
        else:
            self.secex_query = Ymw.query.join(Wld).filter(
                Ymw.wld_id == self.wld_id,
                Ymw.month == 0,
                Ymw.year == self.max_year_query)

    def __secex__(self):
        if not self._secex:
            secex_data = self.secex_query.first_or_404()
            self._secex = secex_data
        return self._secex

    def __secex_list__(self):
        if not self._secex:
            secex_data = self.secex_query.all()
            self._secex = secex_data
        return self._secex

    def __secex_sorted_by_balance__(self):
        if not self._secex_sorted_by_balance:
            self._secex_sorted_by_balance = self.__secex_list__()
            self._secex_sorted_by_balance.sort(key=lambda secex: (
                secex.export_val or 0) - (secex.import_val or 0), reverse=True)
        return self._secex_sorted_by_balance

    def __secex_sorted_by_exports__(self):
        if not self._secex_sorted_by_exports:
            self._secex_sorted_by_exports = self.__secex_list__()
            self._secex_sorted_by_exports.sort(
                key=lambda secex: secex.export_val, reverse=True)
        return self._secex_sorted_by_exports

    def __secex_sorted_by_imports__(self):
        if not self._secex_sorted_by_imports:
            self._secex_sorted_by_imports = self.__secex_list__()
            self._secex_sorted_by_imports.sort(
                key=lambda secex: secex.import_val, reverse=True)
        return self._secex_sorted_by_imports

    def country_name(self):
        base_trade_partner = self.__secex__().wld
        return base_trade_partner.name()

    def location_name(self):
        return Bra.query.filter(Bra.id == self.bra_id).first().name()

    def year(self):
        return self.__secex__().year

    def trade_balance(self):
        export_val = self.__secex__().export_val
        import_val = self.__secex__().import_val
        if export_val is None:
            return import_val
        elif import_val is None:
            return export_val
        else:
            return export_val - import_val

    def total_exported(self):
        export_val = self.__secex__().export_val
        if export_val is None:
            return 0
        else:
            return export_val

    def unity_weight_export_price(self):
        export_val = self.__secex__().export_val
        export_kg = self.__secex__().export_kg
        if export_val is None:
            return None
        else:
            return export_val / export_kg

    def total_imported(self):
        return self.__secex__().import_val

    def unity_weight_import_price(self):
        import_val = self.__secex__().import_val
        import_kg = self.__secex__().import_kg
        if import_val is None:
            return None
        else:
            return import_val / import_kg

    def highest_import_value(self):
        secex = self.__secex_sorted_by_imports__()[0]
        return secex.import_val

    def highest_export_value(self):
        secex = self.__secex_sorted_by_exports__()[0]
        return secex.export_val

    def highest_balance(self):
        secex = self.__secex_sorted_by_balance__()[0]
        export_val = secex.export_val or 0
        import_val = secex.import_val or 0
        return export_val - import_val

    def lowest_balance(self):
        secex = self.__secex_sorted_by_balance__()[-1]
        export_val = secex.export_val or 0
        import_val = secex.import_val or 0
        return export_val - import_val


class TradePartnerMunicipalities(TradePartner):

    def __init__(self, wld_id, bra_id):
        TradePartner.__init__(self, wld_id, bra_id)
        self.max_database_year = db.session.query(func.max(Ymbw.year))
        self.max_year_query = db.session.query(
            func.max(Ymbw.year)).filter_by(wld_id=wld_id).filter(
            Ymbw.year < self.max_database_year)
        if bra_id is not None:
            self.secex_query = Ymbw.query.join(Wld).join(Bra).filter(
                Ymbw.wld_id == self.wld_id,
                Ymbw.bra_id.like(self.bra_id + '%'),
                Ymbw.month == 0,
                Ymbw.year == self.max_year_query,
                func.length(Ymbw.bra_id) == 9)
        else:
            self.secex_query = Ymbw.query.join(Wld).join(Bra).filter(
                Ymbw.wld_id == self.wld_id,
                Ymbw.month == 0,
                Ymbw.year == self.max_year_query,
                func.length(Ymbw.bra_id) == 9)

    def municipality_with_more_imports(self):
        secex = self.__secex_sorted_by_imports__()[0]
        return secex.bra.name()

    def municipality_with_more_imports_state(self):
        secex = self.__secex_sorted_by_imports__()[0]
        return secex.bra.abbreviation

    def municipality_with_more_exports(self):
        secex = self.__secex_sorted_by_exports__()[0]
        return secex.bra.name()

    def municipality_with_more_exports_state(self):
        secex = self.__secex_sorted_by_exports__()[0]
        return secex.bra.abbreviation


class TradePartnerProducts(TradePartner):

    def __init__(self, wld_id, bra_id):
        TradePartner.__init__(self, wld_id, bra_id)
        self.max_database_year = db.session.query(func.max(Ympw.year))
        self.max_year_query = db.session.query(
            func.max(Ympw.year)).filter_by(wld_id=wld_id).filter(
            Ympw.year < self.max_database_year)
        if bra_id is not None:
            self.secex_query = Ymbpw.query.join(Wld).filter(
                Ymbpw.wld_id == self.wld_id,
                Ymbpw.bra_id == self.bra_id,
                Ymbpw.month == 0,
                Ymbpw.hs_id_len == 6,
                Ymbpw.year == self.max_year_query)
        else:
            self.secex_query = Ympw.query.join(Wld).join(Hs).filter(
                Ympw.wld_id == self.wld_id,
                Ympw.month == 0,
                Ympw.hs_id_len == 6,
                Ympw.year == self.max_year_query)

    def product_with_more_exports(self):
        secex = self.__secex_sorted_by_exports__()[0]
        return secex.hs.name()

    def product_with_more_imports(self):
        secex = self.__secex_sorted_by_imports__()[0]
        return secex.hs.name()

    def product_with_highest_balance(self):
        secex = self.__secex_sorted_by_balance__()[0]
        return secex.hs.name()

    def product_with_lowest_balance(self):
        secex = self.__secex_sorted_by_balance__()[-1]
        return secex.hs.name()


class Product:

    def __init__(self, product_id):
        self._secex = None
        self._secex_sorted_by_balance = None
        self._secex_sorted_by_exports = None
        self._secex_sorted_by_imports = None
        self.product_id = product_id
        self.max_database_year = db.session.query(func.max(Ymp.year))

        if product_id is None:
            self.max_year_query = db.session.query(
                func.max(Ymp.year)).filter(Ymp.year < self.max_database_year)
            self.secex_query = Ymp.query.join(Hs).filter(
                Ymp.month == 0,
                Ymp.year == self.max_year_query)
        else:
            self.max_year_query = db.session.query(
                func.max(Ymp.year)).filter_by(hs_id=product_id).filter(
                Ymp.year < self.max_database_year)
            self.secex_query = Ymp.query.join(Hs).filter(
                Ymp.hs_id == self.product_id,
                Ymp.month == 0,
                Ymp.year == self.max_year_query)

    def __secex__(self):
        if not self._secex:
            secex_data = self.secex_query.first_or_404()
            self._secex = secex_data
        return self._secex

    def __secex_list__(self):
        if not self._secex:
            secex_data = self.secex_query.all()
            self._secex = secex_data
        return list(self._secex)

    def __secex_sorted_by_balance__(self):
        self._secex_sorted_by_balance = self.__secex_list__()
        self._secex_sorted_by_balance.sort(key=lambda secex: (
            secex.export_val or 0) - (secex.import_val or 0), reverse=True)
        return self._secex_sorted_by_balance

    def __secex_sorted_by_exports__(self):
        self._secex_sorted_by_exports = self.__secex_list__()
        self._secex_sorted_by_exports = filter(
            lambda secex: secex.export_val, self._secex_sorted_by_exports)
        self._secex_sorted_by_exports.sort(
            key=lambda secex: secex.export_val, reverse=True)
        return self._secex_sorted_by_exports

    def __secex_sorted_by_imports__(self):
        self._secex_sorted_by_imports = self.__secex_list__()
        self._secex_sorted_by_imports = filter(
            lambda secex: secex.import_val, self._secex_sorted_by_imports)
        self._secex_sorted_by_imports.sort(
            key=lambda secex: secex.import_val, reverse=True)
        return self._secex_sorted_by_imports

    def product_name(self):
        product = self.__secex__().hs
        return product.name()

    def year(self):
        return self.max_year_query.first()[0]

    def location_name(self):
        return "Brasil"

    def trade_balance(self):
        export_val = self.__secex__().export_val or 0
        import_val = self.__secex__().import_val or 0
        return export_val - import_val

    def total_exported(self):
        return self.__secex__().export_val

    def unity_weight_export_price(self):
        export_val = self.__secex__().export_val
        export_kg = self.__secex__().export_kg
        return export_val if not export_val else export_val / export_kg

    def total_imported(self):
        return self.__secex__().import_val

    def unity_weight_import_price(self):
        import_val = self.__secex__().import_val
        import_kg = self.__secex__().import_kg
        return import_val if not import_val else import_val / import_kg

    def highest_import_value(self):
        try:
            secex = self.__secex_sorted_by_imports__()[0]
        except IndexError:
            return None
        else:
            return secex.import_val

    def highest_export_value(self):
        try:
            secex = self.__secex_sorted_by_exports__()[0]
        except IndexError:
            return None
        else:
            return secex.export_val

    def highest_import_value_name(self):
        try:
            secex = self.__secex_sorted_by_imports__()[0]
        except IndexError:
            return None
        else:
            return secex.hs.name()

    def highest_export_value_name(self):
        try:
            secex = self.__secex_sorted_by_exports__()[0]
        except IndexError:
            return None
        else:
            return secex.hs.name()

    def product_complexity(self):
        product_complexity = self.__secex__()
        return product_complexity.pci

    def export_value_growth_in_five_years(self):
        export_value_growth_in_five_years = self.__secex__()
        return export_value_growth_in_five_years.export_val_growth_5

    def all_imported(self):
        total_imported = db.session.query(func.sum(Ymb.import_val)).filter_by(
            year=self.max_year_query,
            month=0,
            bra_id_len=1).one()
        return float(total_imported[0])

    def all_exported(self):
        total_exported = db.session.query(func.sum(Ymb.export_val)).filter_by(
            year=self.max_year_query,
            month=0,
            bra_id_len=1).one()
        return float(total_exported[0])

    def all_trade_balance(self):
        return self.all_exported() - self.all_imported()


class ProductTradePartners(Product):

    def __init__(self, product_id, bra_id):
        Product.__init__(self, product_id)
        self.max_database_year = db.session.query(func.max(Ympw.year))
        self.max_year_query = db.session.query(
            func.max(Ympw.year)).filter_by(hs_id=product_id).filter(
            Ympw.year < self.max_database_year)
        self.secex_query = Ympw.query.join(Wld).filter(
            Ympw.hs_id == self.product_id,
            Ympw.wld_id_len == 5,
            Ympw.month == 0,
            Ympw.year == self.max_year_query
        )

        if bra_id:
            self.bra_id = bra_id
            self.max_year_query = db.session.query(
                func.max(Ymbpw.year)).filter_by(
                hs_id=product_id, bra_id=bra_id).filter(
                Ympw.year < self.max_database_year)
            self.secex_query = Ymbpw.query.join(Wld).filter(
                Ymbpw.hs_id == self.product_id,
                Ymbpw.year == self.max_year_query,
                Ymbpw.wld_id_len == 5,
                Ymbpw.bra_id == self.bra_id,
                Ymbpw.month == 0)

    def destination_with_more_exports(self):
        try:
            secex = self.__secex_sorted_by_exports__()[0]
        except IndexError:
            return None
        else:
            return secex.wld.name()

    def origin_with_more_imports(self):
        try:
            secex = self.__secex_sorted_by_imports__()[0]
        except IndexError:
            return None
        else:
            return secex.wld.name()


class ProductMunicipalities(Product):

    def __init__(self, product_id, bra_id):
        Product.__init__(self, product_id)
        self.max_database_year = db.session.query(func.max(Ymbp.year))
        self.max_year_query = db.session.query(
            func.max(Ymbp.year)).filter_by(hs_id=product_id).filter(
            Ymbp.year < self.max_database_year)
        self.secex_query = Ymbp.query.join(Bra).filter(
            Ymbp.hs_id == self.product_id,
            Ymbp.bra_id_len == 9,
            Ymbp.month == 0,
            Ymbp.year == self.max_year_query,
        )

        if bra_id:
            self.bra_id = bra_id
            self.max_year_query = db.session.query(
                func.max(Ymbp.year)).filter_by(
                hs_id=product_id, bra_id=bra_id).filter(
                Ymbp < self.max_database_year)
            self.secex_query = Ymbp.query.join(Bra).filter(
                Ymbp.hs_id == self.product_id,
                Ymbp.year == self.max_year_query,
                Ymbp.bra_id_len == 9,
                Ymbp.bra_id.like(str(self.bra_id) + '%'),
                Ymbp.month == 0)

    def municipality_with_more_exports(self):
        try:
            secex = self.__secex_sorted_by_exports__()[0]
        except IndexError:
            return None
        else:
            return secex.bra.name()

    def municipality_with_more_exports_state(self):
        try:
            secex = self.__secex_sorted_by_exports__()[0]
        except IndexError:
            return None
        else:
            return secex.bra.abbreviation

    def municipality_with_more_imports(self):
        try:
            secex = self.__secex_sorted_by_imports__()[0]
        except IndexError:
            return None
        else:
            return secex.bra.name()

    def municipality_with_more_imports_state(self):
        try:
            secex = self.__secex_sorted_by_imports__()[0]
        except IndexError:
            return None
        else:
            return secex.bra.abbreviation


class ProductLocations(Product):

    def __init__(self, product_id, bra_id):
        self._secex = None
        self.bra_id = bra_id
        self.product_id = product_id
        self.max_database_year = db.session.query(func.max(Ymbp.year))
        self.max_year_query = db.session.query(
            func.max(Ymbp.year)).filter_by(
            hs_id=product_id, bra_id=bra_id).filter(
            Ymbp.year < self.max_database_year)
        self.secex_query = Ymbp.query.filter(
            Ymbp.hs_id == self.product_id,
            Ymbp.bra_id == self.bra_id,
            Ymbp.month == 0,
            Ymbp.year == self.max_year_query
        )

    def location_name(self):
        return Bra.query.filter(Bra.id == self.bra_id).first().name()

    def rca_wld(self):
        secex = self.__secex__()
        return secex.rca_wld

    def distance_wld(self):
        secex = self.__secex__()
        return secex.distance_wld

    def opp_gain_wld(self):
        secex = self.__secex__()
        return secex.opp_gain_wld


class Location:

    def __init__(self, bra_id):
        self._secex = None
        self._secex_sorted_by_exports = None
        self._secex_sorted_by_imports = None
        self._secex_sorted_by_distance = None
        self._secex_sorted_by_opp_gain = None
        self.bra_id = bra_id
        self.max_database_year = db.session.query(func.max(Ymbp.year))
        self.max_year_query = db.session.query(
            func.max(Ymbp.year)).filter_by(bra_id=self.bra_id).filter(
            Ymbp.year < self.max_database_year)
        self.secex_query = Ymbp.query.join(Hs).filter(
            Ymbp.bra_id == self.bra_id,
            Ymbp.month == 0,
            Ymbp.hs_id_len == 6,
            Ymbp.year == self.max_year_query)

    def __secex__(self):
        if not self._secex:
            secex_data = self.secex_query.first_or_404()
            self._secex = secex_data
        return self._secex

    def __secex_list__(self):
        if not self._secex:
            secex_data = self.secex_query.all()
            self._secex = secex_data
        return self._secex

    def __secex_sorted_by_exports__(self):
        if not self._secex_sorted_by_exports:
            self._secex_sorted_by_exports = self.__secex_list__()
            self._secex_sorted_by_exports.sort(
                key=lambda secex: secex.export_val, reverse=True)
        return self._secex_sorted_by_exports

    def __secex_sorted_by_imports__(self):
        if not self._secex_sorted_by_imports:
            self._secex_sorted_by_imports = self.__secex_list__()
            self._secex_sorted_by_imports.sort(
                key=lambda secex: secex.import_val, reverse=True)
        return self._secex_sorted_by_imports

    def __secex_sorted_by_distance__(self):
        if not self._secex_sorted_by_distance:
            not_nulls_list = []
            for i in self.__secex_list__():
                if i.distance is not None:
                    not_nulls_list.append(i)
            not_nulls_list.sort(
                key=lambda secex: secex.distance_wld, reverse=False)
            self._secex_sorted_by_distance = not_nulls_list
        return self._secex_sorted_by_distance

    def __secex_sorted_by_opp_gain__(self):
        if not self._secex_sorted_by_opp_gain:
            not_nulls_list = []
            for i in self.__secex_list__():
                if i.opp_gain is not None:
                    not_nulls_list.append(i)
            not_nulls_list.sort(
                key=lambda secex: secex.opp_gain_wld, reverse=True)
            self._secex_sorted_by_opp_gain = not_nulls_list
        return self._secex_sorted_by_opp_gain

    def year(self):
        return self.max_year_query.first()[0]

    def main_product_by_export_value(self):
        try:
            secex = self.__secex_sorted_by_exports__()[0]
        except IndexError:
            return None
        else:
            return secex.export_val

    def main_product_by_export_value_name(self):
        try:
            secex = self.__secex_sorted_by_exports__()[0]
        except IndexError:
            return None
        else:
            return secex.hs.name()

    def main_product_by_import_value(self):
        try:
            secex = self.__secex_sorted_by_imports__()[0]
        except IndexError:
            return None
        else:
            return secex.import_val

    def main_product_by_import_value_name(self):
        try:
            secex = self.__secex_sorted_by_imports__()[0]
        except IndexError:
            return None
        else:
            return secex.hs.name()

    def total_exports(self):
        try:
            export_sum = 0
            secex = self.__secex_sorted_by_exports__()
            for i in secex:
                if i.export_val is not None:
                    export_sum += i.export_val
        except IndexError:
            return None
        else:
            return export_sum

    def total_imports(self):
        try:
            import_sum = 0
            secex = self.__secex_sorted_by_imports__()
            for i in secex:
                if i.import_val is not None:
                    import_sum += i.import_val
        except IndexError:
            return None
        else:
            return import_sum

    def less_distance_by_product(self):
        try:
            secex = self.__secex_sorted_by_distance__()[0]
        except IndexError:
            return None
        else:
            return secex.distance_wld

    def less_distance_by_product_name(self):
        try:
            secex = self.__secex_sorted_by_distance__()[0]
        except IndexError:
            return None
        else:
            return secex.hs.name()

    def opportunity_gain_by_product(self):
        try:
            secex = self.__secex_sorted_by_opp_gain__()[0]
        except IndexError:
            return None
        else:
            return secex.opp_gain_wld

    def opportunity_gain_by_product_name(self):
        try:
            secex = self.__secex_sorted_by_opp_gain__()[0]
        except IndexError:
            return None
        else:
            return secex.hs.name()


class LocationWld(Location):

    def __init__(self, bra_id):
        Location.__init__(self, bra_id)
        self.bra_id = bra_id
        self.max_database_year = db.session.query(func.max(Ymbw.year))
        self.max_year_query = db.session.query(
            func.max(Ymbw.year)).filter_by(bra_id=self.bra_id).filter(
            Ymbw.year < self.max_database_year)
        self.secex_query = Ymbw.query.join(Wld).filter(
            Ymbw.bra_id == self.bra_id,
            Ymbw.month == 0,
            Ymbw.wld_id_len == 5,
            Ymbw.year == self.max_year_query)

    def main_destination_by_export_value(self):
        try:
            secex = self.__secex_sorted_by_exports__()[0]
        except IndexError:
            return None
        else:
            return secex.export_val

    def main_destination_by_export_value_name(self):
        try:
            secex = self.__secex_sorted_by_exports__()[0]
        except IndexError:
            return None
        else:
            return secex.wld.name()

    def main_destination_by_import_value(self):
        try:
            secex = self.__secex_sorted_by_imports__()[0]
        except IndexError:
            return None
        else:
            return secex.import_val

    def main_destination_by_import_value_name(self):
        try:
            secex = self.__secex_sorted_by_imports__()[0]
        except IndexError:
            return None
        else:
            return secex.wld.name()


class LocationEciRankings:

    def __init__(self, bra_id):
        self._secex = None
        self._secex_sorted_by_eci = None
        self.bra_id = bra_id
        self.max_database_year = db.session.query(func.max(Ymb.year))
        self.max_year_query = db.session.query(
            func.max(Ymb.year)).filter_by(bra_id=self.bra_id).filter(
            Ymb.year < self.max_database_year)
        self.secex_query = Ymb.query.filter(
            Ymb.year == self.max_year_query,
            Ymb.month == 0,
            func.length(Ymb.bra_id) == 5)

    def __secex_sorted_by_eci__(self):
        if not self._secex_sorted_by_eci:
            self._secex_sorted_by_eci = self.__secex_list__()
            self._secex_sorted_by_eci.sort(
                key=lambda secex: secex.eci, reverse=True)
        return self._secex_sorted_by_eci

    def __secex_list__(self):
        if not self._secex:
            secex_data = self.secex_query.all()
            self._secex = secex_data
        return self._secex

    def eci_rank(self):
        eci_list = self.__secex_sorted_by_eci__()
        rank = 1
        for eci in eci_list:
            if eci.bra_id == self.bra_id:
                return rank
                break
            rank += 1