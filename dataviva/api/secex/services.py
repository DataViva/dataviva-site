from dataviva.api.attrs.models import Wld, Bra, Hs
from dataviva.api.secex.models import Ymw, Ymbw, Ympw
from dataviva import db
from flask import g
from sqlalchemy.sql.expression import func, desc, asc

class TradePartner:


    def __init__(self, wld_id):
        self._secex = None
        self.wld_id = wld_id

        self.max_year_query = db.session.query(func.max(Ymw.year)).filter_by(wld_id=wld_id)

        self.secex_query = Ymw.query.join(Wld).filter(
            Ymw.wld_id == self.wld_id,
            Ymw.month == 0,
            Ymw.year == self.max_year_query)

    def __secex__(self):
        if not self._secex:
            secex_data = self.secex_query.one()
            self._secex = secex_data

        return self._secex

    def country_name(self):
        base_trade_partner = self.__secex__().wld
        return base_trade_partner.name()

    def year(self):
        return self.__secex__().year

    def trade_balance(self):
        export_val = self.__secex__().export_val
        import_val = self.__secex__().import_val

        return export_val - import_val

    def total_exported(self):
        return self.__secex__().export_val

    def unity_weight_export_price(self):
        export_val = self.__secex__().export_val
        export_kg = self.__secex__().export_kg

        return export_val / export_kg

    def total_imported(self):
        return self.__secex__().import_val

    def unity_weight_import_price(self):
        import_val = self.__secex__().import_val
        import_kg = self.__secex__().import_kg

        return import_val / import_kg

class TradePartnerMunicipalityByExport(TradePartner):


    def __init__(self, wld_id):
        TradePartner.__init__(self, wld_id)
        self.max_year_query = db.session.query(func.max(Ymbw.year)).filter_by(wld_id=wld_id)
        self.secex_query = Ymbw.query.join(Bra).filter(
            Ymbw.wld_id == self.wld_id,
            Ymbw.month == 0,
            Ymbw.year == self.max_year_query,
            func.length(Ymbw.bra_id) == 9).order_by(desc(Ymbw.export_val)).limit(1)

    def municipality_with_more_exports(self):
        return self.__secex__().name()

    def highest_export_value_by_municipality(self):
        return self.__secex__().export_val

class TradePartnerMunicipalityByImport(TradePartner):


    def __init__(self, wld_id):
        TradePartner.__init__(self, wld_id)
        self.max_year_query = db.session.query(func.max(Ymbw.year)).filter_by(wld_id=wld_id)
        self.secex_query = Ymbw.query.join(Bra).filter(
            Ymbw.wld_id == self.wld_id,
            Ymbw.month == 0,
            Ymbw.year == self.max_year_query,
            func.length(Ymbw.bra_id) == 9).order_by(desc(Ymbw.import_val)).limit(1)

    def municipality_with_more_imports(self):
        return self.__secex__().name()

    def highest_import_value_by_municipality(self):
        return self.__secex__().import_val

class TradePartnerProductByImport(TradePartner):

    def __init__(self, wld_id):
        TradePartner.__init__(self, wld_id)
        self.max_year_query = db.session.query(func.max(Ympw.year)).filter_by(wld_id=wld_id)
        self.secex_query = Ympw.query.join(Hs).filter(
            Ympw.wld_id == self.wld_id,
            Ympw.month == 0,
            Ympw.hs_id_len == 6,
            Ympw.year == self.max_year_query).order_by(desc(Ympw.import_val)).limit(1)

    def product_with_more_imports(self):
        return self.__secex__().name()

    def highest_import_value_by_product(self):
        return self.__secex__().import_val

class TradePartnerProductByExport(TradePartner):

    def __init__(self, wld_id):
        TradePartner.__init__(self, wld_id)
        self.max_year_query = db.session.query(func.max(Ympw.year)).filter_by(wld_id=wld_id)
        self.secex_query = Ympw.query.join(Hs).filter(
            Ympw.wld_id == self.wld_id,
            Ympw.month == 0,
            Ympw.hs_id_len == 6,
            Ympw.year == self.max_year_query).order_by(desc(Ympw.export_val)).limit(1)

    def product_with_more_exports(self):
        return self.__secex__().name()

    def highest_export_value_by_product(self):
        return self.__secex__().export_val


class TradePartnerProductByHighestBalance(TradePartner):


    def __init__(self, wld_id):
        TradePartner.__init__(self, wld_id)
        self.max_year_query = db.session.query(func.max(Ympw.year)).filter_by(wld_id=wld_id)
        ympw_highest_balance_query = Ympw.query.join(Hs).filter(
            Ympw.wld_id == self.wld_id,
            Ympw.month == 0,
            Ympw.hs_id_len == 6,
            Ympw.year == self.max_year_query).order_by(desc(Ympw.export_val-Ympw.import_val)).limit(1)

    def product_with_highest_balance(self):
        return self.__secex__().name()

    def highest_balance_by_product(self):
        return self.__secex__().export_val - self.__secex__().import_val


class TradePartnerProductByLowestBalance(TradePartner):


    def __init__(self, wld_id):
        TradePartner.__init__(self, wld_id)
        self.max_year_query = db.session.query(func.max(Ympw.year)).filter_by(wld_id=wld_id)
        ympw_highest_balance_query = Ympw.query.join(Hs).filter(
            Ympw.wld_id == self.wld_id,
            Ympw.month == 0,
            Ympw.hs_id_len == 6,
            Ympw.year == self.max_year_query).order_by(asc(Ympw.export_val-Ympw.import_val)).limit(1)

    def product_with_lowest_balance(self):
        return self.__secex__().name()

    def lowest_balance_by_product(self):
        return self.__secex__().export_val - self.__secex__().import_val
