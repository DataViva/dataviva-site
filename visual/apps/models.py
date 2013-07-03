from flask import g
from visual import db
from visual.utils import AutoSerialize
from visual.attrs.models import Bra, Isic, Hs, Cbo, Wld

build_ui = db.Table('apps_build_ui',
         db.Column('build_id', db.Integer,db.ForeignKey('apps_build.id')),
         db.Column('ui_id', db.Integer,db.ForeignKey('apps_ui.id'))
)

class Build(db.Model):

    __tablename__ = 'apps_build'
    
    id = db.Column(db.Integer, primary_key = True)
    viz_whiz = db.Column(db.String(20))
    filter1 = db.Column(db.String(20))
    filter2 = db.Column(db.String(20))
    output = db.Column(db.String(20))
    type = db.Column(db.String(20))
    name = db.Column(db.String(20))
    color = db.Column(db.String(7))
    dataset = db.Column(db.String(20))
    
    ui = db.relationship('UI', secondary=build_ui, backref=db.backref('Builds'), lazy='dynamic')
    
    def get_ui(self, ui_type):
        return self.ui.filter(UI.type == ui_type).first()
    
    def get_bra_and_filters(self, **kwargs):
        defaults = {"cbo":"1210", "hs":"178703", "isic":"c1410", "wld":"aschn", "bra":"mg"}
        result = {"bra":None, "filter1":None, "filter2":None}
        
        for f in result.keys():
            if f == "bra":
                if 'bra' in kwargs:
                    bra = kwargs['bra'] or defaults['bra']
                else:
                    bra = defaults['bra']
                result['bra'] = bra
            
            else:
                filter_type = getattr(self, f)
                if "all" not in filter_type:
                    filter_type = filter_type[filter_type.find("<")+1:filter_type.find(">")]
                    if filter_type in kwargs:
                        result[f] = {"filter_type":filter_type, "id":kwargs[filter_type] or defaults[filter_type]}
                    else:
                        result[f] = {"filter_type":filter_type, "id":defaults[filter_type]}
                else:
                    result[f] = filter_type
        
        return result
    
    '''Returns the URL for the specific build.'''
    def url(self, **kwargs):
        
        filters = self.get_bra_and_filters(**kwargs)
        bra = filters["bra"]
        if filters["filter1"] == "all": filter1 = "all"
        else: filters["filter1"]["id"]
        if filters["filter2"] == "all": filter2 = "all"
        else: filters["filter2"]["id"]
        
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.viz_whiz, 
                                                self.dataset, bra, 
                                                filter1, filter2, 
                                                self.output)
        return url

    '''Returns the data URL for the specific build. This URL will return the 
    data required for building a viz of this app.
    '''
    def data_url(self, **kwargs):

        filters = self.get_bra_and_filters(**kwargs)
        
        bra = filters["bra"]
        if self.output == "bra":
            bra = bra + ".8"
        
        filter1 = filters["filter1"]
        if filter1 == "all":
            if self.output == "isic":
                filter1 = "show.5"
            elif self.output == "hs":
                filter1 = "show.6"
        else:
            filter1 = filters["filter1"]["id"]
        
        filter2 = filters["filter2"]
        if filter2 == "all":
            if self.output == "cbo":
                filter2 = "show.4"
            elif self.output == "wld":
                filter2 = "show.5"
        else:
            filter2 = filters["filter2"]["id"]

        filter2 = "all" if filters["filter2"] == "all" else filters["filter2"]["id"]
        filter2 = "show" if self.output == "cbo" or self.output == "wld" else filter2

        data_url = '{0}/all/{1}/{2}/{3}/'.format(self.dataset, bra, filter1, filter2)
        return data_url
    
    '''Returns the english language title of this build.'''
    def title(self, **kwargs):
        
        filters = self.get_bra_and_filters(**kwargs)
        bra = filters["bra"]
        f1 = filters["filter1"]
        f2 = filters["filter2"]
        
        bra = Bra.query.get_or_404(bra)
        filters = []
        if f1 != "all":
            f1 = Isic.query.get_or_404(f1["id"]) if self.dataset == "rais" else Hs.query.get_or_404(f1["id"])
            filters.append(f1)
        if f2 != "all":
            f2 = Cbo.query.get_or_404(f2["id"]) if self.dataset == "rais" else Wld.query.get_or_404(f2["id"])
            filters.append(f2)
        
        if self.output == "hs": 
            output_name = "Product";    output_name_pl = "Products"
        if self.output == "isic": 
            output_name = "Industry";   output_name_pl = "Industries"
        if self.output == "cbo": 
            output_name = "Occupation"; output_name_pl = "Occupations"
        if self.output == "wld": 
            output_name = "Country";    output_name_pl = "Countries"
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

    def __repr__(self):
        return '<Build %r/%r/%r/%r>' % (self.viz_whiz, self.filter1, 
                                            self.filter2, self.output)

class UI(db.Model):

    __tablename__ = 'apps_ui'

    id = db.Column(db.Integer, db.ForeignKey(Build.id), primary_key = True)
    type = db.Column(db.String(20))
    values = db.Column(db.String(255))
    
    def __repr__(self):
        return '<Build %r: %r>' % (self.type, self.values)