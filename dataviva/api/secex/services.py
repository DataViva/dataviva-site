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

class TradePartnerByLocation(TradePartner):

   def __init__(self, wld_id, bra_id):
        super(TradePartnerByLocation, self).__init__(wld_id)
        self.bra_id = bra_id
        self.max_year_query = db.session.query(func.max(Ymbw.year)).filter_by(wld_id=wld_id)
        self.secex_query = Ymbw.query.join(Bra).filter(
            Ymbw.wld_id == self.wld_id,
            Ymbw.month == 0,
            Ymbw.year == self.max_year_query,
            func.length(Ymbw.bra_id) == 9).order_by(desc(Ymbw.export_val))

    def municipality_with_more_exports(self):
        ymbw_municipality_export_query = Ymbw.query.join(Bra).filter(
            Ymbw.wld_id == self.wld_id,
            Ymbw.month == 0,
            Ymbw.year == self.max_year_query,
            func.length(Ymbw.bra_id) == 9).order_by(desc(Ymbw.export_val)).limit(1)

        ymbw_municipality_export_data = ymbw_municipality_export_query.values(
            Bra.name_pt,
            Ymbw.export_val)

        municipality = {}

        for name_pt, export_val in ymbw_municipality_export_data:
            municipality['name'] = name_pt
            municipality['value'] = export_val

        return municipality

    def municipality_with_more_imports(self):
        ymbw_municipality_import_query = Ymbw.query.join(Bra).filter(
            Ymbw.wld_id == self.wld_id,
            Ymbw.month == 0,
            Ymbw.year == self.ymbw_max_year,
            func.length(Ymbw.bra_id) == 9).order_by(desc(Ymbw.import_val)).limit(1)

        ymbw_municipality_import_data = ymbw_municipality_import_query.values(
            Bra.name_pt,
            Ymbw.import_val)

        municipality = {}

        for name_pt, import_val in ymbw_municipality_import_data:
            municipality['name'] = name_pt
            municipality['value'] = import_val

        return municipality

    def product_with_more_exports(self):
        ympw_product_export_query = Ympw.query.join(Hs).filter(
            Ympw.wld_id == self.wld_id,
            Ympw.month == 0,
            Ympw.hs_id_len == 6,
            Ympw.year == self.ympw_max_year).order_by(desc(Ympw.export_val)).limit(1)

        ympw_product_export_data = ympw_product_export_query.values(
            Hs.name_pt,
            Ympw.export_val)

        product = {}

        for name_pt, export_val in ympw_product_export_data:
            product['name'] = name_pt
            product['value'] = export_val

        return product

    def product_with_more_imports(self):

        ympw_product_import_query = Ympw.query.join(Hs).filter(
            Ympw.wld_id == self.wld_id,
            Ympw.month == 0,
            Ympw.hs_id_len == 6,
            Ympw.year == self.ympw_max_year).order_by(desc(Ympw.import_val)).limit(1)

        ympw_product_import_data = ympw_product_import_query.values(
            Hs.name_pt,
            Ympw.import_val)

        product = {}

        for name_pt, import_val in ympw_product_import_data:
            product['name'] = name_pt
            product['value'] = import_val

        return product

    def product_with_highest_balance(self):
        ympw_highest_balance_query = Ympw.query.join(Hs).filter(
            Ympw.wld_id == self.wld_id,
            Ympw.month == 0,
            Ympw.hs_id_len == 6,
            Ympw.year == self.ympw_max_year).order_by(desc(Ympw.export_val-Ympw.import_val)).limit(1)

        ympw_highest_balance_data = ympw_highest_balance_query.values(
            Hs.name_pt,
            (Ympw.export_val - Ympw.import_val))

        product = {}

        for name_pt, trade_balance in ympw_highest_balance_data:
            product['name'] = name_pt
            product['value'] = trade_balance

        return product

    def product_with_lowest_balance(self):
        ympw_lowest_balance_query = Ympw.query.join(Hs).filter(
            Ympw.wld_id == self.wld_id,
            Ympw.month == 0,
            Ympw.hs_id_len == 6,
            Ympw.year == self.ympw_max_year).order_by(asc(Ympw.export_val-Ympw.import_val)).limit(1)

        ympw_lowest_balance_data = ympw_lowest_balance_query.values(
            Hs.name_pt,
            (Ympw.export_val - Ympw.import_val))

        product = {}

        for name_pt, trade_balance in ympw_lowest_balance_data:
            product['name'] = name_pt
            product['value'] = trade_balance

        return product