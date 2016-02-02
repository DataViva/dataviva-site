from dataviva.api.attrs.models import Hs, Bra, Wld
from dataviva.api.secex.models import Ymp, Ymbp, Ympw, Ymbpw
from dataviva import db
from sqlalchemy import func, desc

class Product:
    def __init__(self, bra_id, product_id):
        self.bra_id = bra_id
        self.product_id = product_id
        self.ymp_max_year_query = db.session.query(
            func.max(Ymp.year)).filter_by(hs_id=product_id)
        self.ymbp_max_year_query = db.session.query(
            func.max(Ymbp.year)).filter_by(hs_id=product_id)
        self.ympw_max_year_query = db.session.query(
            func.max(Ympw.year)).filter_by(hs_id=product_id)
        self.ymbpw_max_year_query = db.session.query(
            func.max(Ymbpw.year)).filter_by(hs_id=product_id, bra_id=bra_id)


        self.product = {}

    def name(self):
        name = Hs.query.filter(
            Hs.id == self.product_id).first().name()
        return {'name': name}

    def pci(self):
        ymp_pci_query = Ymp.query.filter(Ymp.hs_id==self.product_id,
                                     Ymp.year==self.ymp_max_year_query,
                                     Ymp.month==0).limit(1)
        pci = ymp_pci_query.one().pci
        return {'pci': pci}

    def brazil_section_position(self):
        ymp_query = Ymp.query.filter(
            Ymp.hs_id==self.product_id,
            Ymp.year==self.ymp_max_year_query,
            Ymp.month==0
        ).limit(1)
    
        ymp_data = ymp_query.values(
            Ymp.year,
            Ymp.export_val,
            Ymp.import_val,
            Ymp.export_kg,
            Ymp.import_kg
        )
    
        for year, export_val, import_val, export_kg, import_kg in ymp_data:
            self.product['year'] = year
            self.product['export_val'] = export_val
            self.product['import_val'] = import_val
            self.product['export_kg'] = export_kg
            self.product['import_kg'] = import_kg
            self.product['trade_balance'] = export_val - import_val
            self.product['export_net_weight'] = export_kg / export_val
            self.product['import_net_weight'] = import_kg / import_val
    
        return self.product

    def brazil_export(self):
        ymbp_query = Ymbp.query.join(Bra).filter(
            Ymbp.hs_id==self.product_id,
            Ymbp.year==self.ymbp_max_year_query,
            Ymbp.bra_id_len==9,
            Ymbp.month==0
        ).order_by(desc(Ymbp.export_val)).limit(1)        
        
        ymbp_bra_data = ymbp_query.values(
            Bra.name_pt,
            Ymbp.export_val
        )   

        for name_pt, export_val in ymbp_bra_data:
            self.product['munic_name_export'] = name_pt
            self.product['munic_export_value'] = export_val        
        return self.product
    
    def brazil_import(self):
        ymbp_query = Ymbp.query.join(Bra).filter(
            Ymbp.hs_id==self.product_id,
            Ymbp.year==self.ymbp_max_year_query,
            Ymbp.bra_id_len==9,
            Ymbp.month==0
        ).order_by(desc(Ymbp.import_val)).limit(1)
    
        ymbp_bra_data = ymbp_query.values(
            Bra.name_pt,
            Ymbp.import_val
        )
    
        for name_pt, import_val in ymbp_bra_data:
            self.product['munic_name_import'] = name_pt
            self.product['munic_import_value'] = import_val
    
        return self.product
    
    def brazil_dest_export(self):
        ympw_query = Ympw.query.join(Wld).filter(
            Ympw.hs_id==self.product_id,
            Ympw.year==self.ympw_max_year_query,
            Ympw.wld_id_len==5,
            Ympw.month==0
        ).order_by(desc(Ympw.export_val)).limit(1)
    
        ympw_wld_data = ympw_query.values(
            Wld.name_pt,
            Ympw.export_val
        )
    
        for name_pt, export_val in ympw_wld_data:
            self.product['dest_name_export'] = name_pt
            self.product['dest_export_value'] = export_val
    
        return self.product
    
    def brazil_src_import(self):
        ympw_query = Ympw.query.join(Wld).filter(
            Ympw.hs_id==self.product_id,
            Ympw.year==self.ympw_max_year_query,
            Ympw.wld_id_len==5,
            Ympw.month==0
        ).order_by(desc(Ympw.import_val)).limit(1)
    
        ympw_wld_data = ympw_query.values(
            Wld.name_pt,
            Ympw.import_val
        )
    
        for name_pt, import_val in ympw_wld_data:
            self.product['src_name_import'] = name_pt
            self.product['src_import_value'] = import_val
    
        return self.product

    def location_postion(self):
        ymbp_query = Ymbp.query.filter(
            Ymbp.hs_id==self.product_id,
            Ymbp.year==self.ymbp_max_year_query,
            Ymbp.bra_id==self.bra_id,
            Ymbp.month==0
        ).limit(1)
    
        ymbp_data = ymbp_query.values(
            Ymbp.year,
            Ymbp.export_val,
            Ymbp.import_val,
            Ymbp.export_kg,
            Ymbp.import_kg,
            Ymbp.rca_wld,
            Ymbp.distance_wld,
            Ymbp.opp_gain_wld
        )
    
        for year, export_val, import_val, export_kg, import_kg, rca_wld, distance_wld, opp_gain_wld in ymbp_data:
            export_val = export_val or 0
            import_val = import_val or 0
            export_kg = export_kg or 0
            import_kg = import_kg or 0
    
            self.product['year'] = year
            self.product['export_val'] = export_val
            self.product['import_val'] = import_val
            self.product['export_kg'] = export_kg
            self.product['import_kg'] = import_kg
            self.product['trade_balance'] = export_val - import_val
    
            if export_val == 0:
                self.product['export_net_weight'] = None
            else:
                self.product['export_net_weight'] = export_kg / export_val
    
            if import_val == 0:
                self.product['import_net_weight'] = None
            else:
                self.product['import_net_weight'] = import_kg / import_val
    
            self.product['rca_wld'] = rca_wld
            self.product['distance_wld'] = distance_wld
            self.product['opp_gain_wld'] = opp_gain_wld

        return self.product

    def location_section(self):
        ymbp_query = Ymbp.query.filter(
            Ymbp.hs_id==self.product_id,
            Ymbp.year==self.ymbp_max_year_query,
            Ymbp.bra_id==self.bra_id,
            Ymbp.month==0
        ).limit(1)
    
        ymbp_data = ymbp_query.values(
            Ymbp.year,
            Ymbp.export_val,
            Ymbp.import_val,
            Ymbp.export_kg,
            Ymbp.import_kg
        )
    
        for year, export_val, import_val, export_kg, import_kg in ymbp_data:
            self.product['year'] = year
            self.product['export_val'] = export_val
            self.product['import_val'] = import_val
            self.product['export_kg'] = export_kg
            self.product['import_kg'] = import_kg
            self.product['trade_balance'] = export_val - import_val
            self.product['export_net_weight'] = export_kg / export_val
            self.product['import_net_weight'] = import_kg / import_val
    
        return self.product
    
    def location_dest_export(self):
        ymbpw_query = Ymbpw.query.join(Wld).filter(
            Ymbpw.hs_id==self.product_id,
            Ymbpw.year==self.ymbpw_max_year_query,
            Ymbpw.wld_id_len==5,
            Ymbpw.bra_id.like(str(self.bra_id)+'%'),
            Ymbpw.month==0
        ).order_by(desc(Ymbpw.export_val)).limit(1)
    
        ymbpw_wld_data = ymbpw_query.values(
            Wld.name_pt,
            Ymbpw.export_val
        )
    
        for name_pt, export_val in ymbpw_wld_data:
            self.product['dest_name_export'] = name_pt
            self.product['dest_export_value'] = export_val
    
        return self.product
    
    def location_src_import(self):
        ymbpw_query = Ymbpw.query.join(Wld).filter(
            Ymbpw.hs_id==self.product_id,
            Ymbpw.year==self.ymbpw_max_year_query,
            Ymbpw.wld_id_len==5,
            Ymbpw.bra_id.like(str(self.bra_id)+'%'),
            Ymbpw.month==0
        ).order_by(desc(Ymbpw.import_val)).limit(1)
    
        ymbpw_wld_data = ymbpw_query.values(
            Wld.name_pt,
            Ymbpw.import_val
        )
    
        for name_pt, import_val in ymbpw_wld_data:
            self.product['src_name_import'] = name_pt
            self.product['src_import_value'] = import_val
    
        return self.product
    
    def location_diff_munic_export(self):
        ymbp_query = Ymbp.query.join(Bra).filter(
            Ymbp.hs_id==self.product_id,
            Ymbp.year==self.ymbp_max_year_query,
            Ymbp.bra_id_len==9,
            Ymbp.bra_id.like(str(self.bra_id)+'%'),
            Ymbp.month==0
        ).order_by(desc(Ymbp.export_val)).limit(1)
    
        ymbp_bra_data = ymbp_query.values(
            Bra.name_pt,
            Ymbp.export_val
        )
    
        for name_pt, export_val in ymbp_bra_data:
            self.product['munic_name_export'] = name_pt
            self.product['munic_export_value'] = export_val
    
        return self.product
    
    def location_diff_munic_import(self):
        ymbp_query = Ymbp.query.join(Bra).filter(
            Ymbp.hs_id==self.product_id,
            Ymbp.year==self.ymbp_max_year_query,
            Ymbp.bra_id_len==9,
            Ymbp.bra_id.like(str(self.bra_id)+'%'),
            Ymbp.month==0
        ).order_by(desc(Ymbp.import_val)).limit(1)
    
        ymbp_bra_data = ymbp_query.values(
            Bra.name_pt,
            Ymbp.import_val
        )
    
        for name_pt, import_val in ymbp_bra_data:
            self.product['munic_name_import'] = name_pt
            self.product['munic_import_value'] = import_val
    
        return self.product