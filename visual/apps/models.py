from flask import g
from visual import db
from visual.utils import AutoSerialize
from visual.attrs.models import Bra, Isic, Hs, Cbo, Wld

import ast

build_ui = db.Table('apps_build_ui',
         db.Column('build_id', db.Integer,db.ForeignKey('apps_build.id')),
         db.Column('ui_id', db.Integer,db.ForeignKey('apps_ui.id'))
)

class Build(db.Model, AutoSerialize):

    __tablename__ = 'apps_build'
    __public__ = ('id', 'type', 'bra', 'filter1', 'filter2', 'output', 'viz_whiz', 'name', 'color', 'dataset')
    
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(20))
    bra = db.Column(db.String(20))
    filter1 = db.Column(db.String(20))
    filter2 = db.Column(db.String(20))
    output = db.Column(db.String(20))
    viz_whiz = db.Column(db.String(20))
    name = db.Column(db.String(20))
    color = db.Column(db.String(7))
    dataset = db.Column(db.String(20))
    
    ui = db.relationship('UI', secondary=build_ui, backref=db.backref('Builds'), lazy='dynamic')
    
    def get_ui(self, ui_type):
        return self.ui.filter(UI.type == ui_type).first()

    def set_bra(self, bra_id):
        if bra_id == "all":
            self.bra = Wld.query.get("sabra")
            self.bra.id = "all"
            self.bra.icon = "/static/img/icons/wld/wld_sabra.png"
        else:
            self.bra = Bra.query.get(bra_id)
            self.bra.icon = "/static/img/icons/bra/bra_{0}.png".format(bra_id[:2])

    def set_filter1(self, filter):
        if self.filter1 == "all":
            self.filter1 = "all"
        elif self.dataset == "rais":
            if Isic.query.get(filter):
                self.filter1 = Isic.query.get(filter)
            else:
                self.filter1 = Isic.query.get('c1410')
        elif self.dataset == "secex":
            if Hs.query.get(filter):
                self.filter1 = Hs.query.get(filter)
            else:
                self.filter1 = Hs.query.get('178703')
    
    def set_filter2(self, filter):
        if self.filter2 == "all":
            self.filter2 = "all"
        elif self.dataset == "rais":
            if Cbo.query.get(filter):
                self.filter2 = Cbo.query.get(filter)
            else:
                self.filter2 = Cbo.query.get('1210')
        elif self.dataset == "secex":
            if Wld.query.get(filter):
                self.filter2 = Wld.query.get(filter)
            else:
                self.filter2 = Wld.query.get('aschn')
        
    '''Returns the URL for the specific build.'''
    def url(self, **kwargs):
        
        # filters = self.get_bra_and_filters(**kwargs)
        # bra = filters["bra"]
        bra = self.bra.id
        if self.filter1 == "all": filter1 = "all"
        else: filter1 = self.filter1.id
        if self.filter2 == "all": filter2 = "all"
        else: filter2 = self.filter2.id
        
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.viz_whiz, 
                                                self.dataset, bra, 
                                                filter1, filter2, 
                                                self.output)
        return url

    '''Returns the data URL for the specific build. This URL will return the 
    data required for building a viz of this app.
    '''
    def data_url(self, **kwargs):
        # filters = self.get_bra_and_filters(**kwargs)
        
        bra = self.bra.id
        if self.output == "bra":
            bra = bra + ".8"
        
        filter1 = self.filter1
        if filter1 == "all":
            if self.output == "isic":
                filter1 = "show.5"
            elif self.output == "hs":
                filter1 = "show.6"
        else:
            filter1 = self.filter1.id
        
        filter2 = self.filter2
        if filter2 == "all":
            if self.output == "cbo":
                filter2 = "show.4"
            elif self.output == "wld":
                filter2 = "show.5"
        else:
            self.filter2.id

        filter2 = "all" if self.filter2 == "all" else self.filter2.id
        filter2 = "show" if self.output == "cbo" or self.output == "wld" else filter2

        data_url = '{0}/all/{1}/{2}/{3}/'.format(self.dataset, bra, filter1, filter2)
        return data_url
    
    '''Returns the english language title of this build.'''
    def title(self, **kwargs):

        bra = self.bra
        f1 = self.filter1
        f2 = self.filter2
        
        # bra = Bra.query.get_or_404(bra)
        filters = []
        if f1 != "all":
            filters.append(f1)
        if f2 != "all":
            filters.append(f2)
        
        if self.output == "hs": 
            output_name = "Product";    output_name_pl = "Product Exports"
        if self.output == "isic": 
            output_name = "Industry";   output_name_pl = "Local Industries"
        if self.output == "cbo": 
            output_name = "Occupation"; output_name_pl = "Occupations"
        if self.output == "wld": 
            output_name = "Trade Partner";    output_name_pl = "Trade Partners"
        if self.output == "bra": 
            output_name = "Location";   output_name_pl = "Locations"

        if self.dataset == "rais":  items = "Local Industries"
        if self.dataset == "secex": items = "Product Exports"

        # if g.locale == "en":
        if True:
            if self.type == "network":
                return output_name + " Space for " + bra.name_en
            elif self.type == "rings":
                return "Connections for " + filters[0].name_en + " in " + bra.name_en
            elif self.type == "bubbles":
                return "Available and required employment for " + filters[0].name_en + " in " + bra.name_en;
            else:
                title = output_name_pl
                if self.output == "isic" or self.output == "cbo" or self.output == "bra":
                    title += " in "
                if self.output == "hs" or self.output == "wld":
                    title += " of "
                title += bra.name_en
                if self.output == "bra" and len(filters) == 1:
                    title += " with " + items

                for i, f in enumerate(filters):
                    if isinstance(f, Isic):
                        article = "employed in" if self.output == "cbo" else "that have"
                        title += " " + article + " the " + f.name_en + " industry"
                    elif isinstance(f, Cbo):
                        article = "that" if i == 0 else "and"
                        title += " " + article + " employ " + f.name_en
                    elif isinstance(f, Hs):
                      trade = "import" if self.output == "wld" else "export"
                      title += " that " + trade + " " + f.name_en
                    elif isinstance(f, Wld):
                      title += " to " + f.name_en
                    elif isinstance(f, Bra):
                      title += " and " + bra2.name_en
                return title
        elif g.locale == "pt":
            pass

    def serialize(self, **kwargs):
        auto_serialized = super(Build, self).serialize()
        # filters = self.get_bra_and_filters(**kwargs)
        auto_serialized["bra"] = self.bra.serialize()
        auto_serialized["filter1"] = "all" if self.filter1 == "all" else self.filter1.serialize()
        auto_serialized["filter2"] = "all" if self.filter2 == "all" else self.filter2.serialize()
        auto_serialized["title"] = self.title()
        auto_serialized["data_url"] = self.data_url()
        auto_serialized["url"] = self.url()
        auto_serialized["ui"] = [ui.serialize() for ui in self.ui.all()]
        return auto_serialized

    def __repr__(self):
        return '<Build %r/%r/%r/%r>' % (self.viz_whiz, self.filter1, 
                                            self.filter2, self.output)

class UI(db.Model, AutoSerialize):

    __tablename__ = 'apps_ui'
    __public__ = ("type","values")

    id = db.Column(db.Integer, db.ForeignKey(Build.id), primary_key = True)
    type = db.Column(db.String(20))
    values = db.Column(db.String(255))
    
    def serialize(self, **kwargs):
        auto_serialized = super(UI, self).serialize()
        auto_serialized["values"] = ast.literal_eval(self.values)
        return auto_serialized
    
    def __repr__(self):
        return '<Build %r: %r>' % (self.type, self.values)