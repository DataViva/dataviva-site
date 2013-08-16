from flask import g
from visual import db
from visual.utils import AutoSerialize
from visual.attrs.models import Bra, Isic, Hs, Cbo, Wld

import ast, re

build_ui = db.Table('apps_build_ui',
         db.Column('build_id', db.Integer,db.ForeignKey('apps_build.id')),
         db.Column('ui_id', db.Integer,db.ForeignKey('apps_ui.id'))
)

class App(db.Model, AutoSerialize):

    __tablename__ = 'apps_app'
    
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(20))
    title = db.Column(db.String(20))
    viz_whiz = db.Column(db.String(20))
    color = db.Column(db.String(7))

class Build(db.Model, AutoSerialize):

    __tablename__ = 'apps_build'
    __public__ = ('id', 'type', 'bra', 'filter1', 'filter2', 'output', 'viz_whiz', 'name', 'color', 'dataset')
    
    id = db.Column(db.Integer, primary_key = True)
    dataset = db.Column(db.String(20))
    bra = db.Column(db.String(20))
    filter1 = db.Column(db.String(20))
    filter2 = db.Column(db.String(20))
    output = db.Column(db.String(20))
    title_en = db.Column(db.String(120))
    title_pt = db.Column(db.String(120))
    app_id = db.Column(db.Integer, db.ForeignKey(App.id))
    
    ui = db.relationship('UI', secondary=build_ui, 
            backref=db.backref('Builds'), lazy='dynamic')
    app = db.relationship('App',
            backref=db.backref('Builds', lazy='dynamic'))
    
    def get_ui(self, ui_type):
        return self.ui.filter(UI.type == ui_type).first()

    def set_bra(self, bra_id):
        '''If build requires 2 bras and only 1 is given, supply a 2nd'''
        if isinstance(self.bra, list):
            return
        if "+" in self.bra and "+" not in bra_id:
            if bra_id == "sp":
                bra_id = bra_id + "+mg"
            else:
                bra_id = bra_id + "+sp"
        elif "+" not in self.bra and "+" in bra_id:
            bra_id = bra_id.split("+")[0]
        self.bra = []
        for i, b in enumerate(bra_id.split("+")):
            if b == "all":
                self.bra.append(Wld.query.get("sabra"))
                self.bra[i].id = "all"
            else:
                if "." in b:
                    split = b.split(".")
                    b = split[0]
                    dist = split[1]
                else:
                    dist = 0
                state = b[:2]
                if self.output == "bra":
                    b = state
                self.bra.append(Bra.query.get(b))
                self.bra[i].distance = dist

    def set_filter1(self, filter):
        if self.filter1 != "all":
            if self.dataset == "rais":
                self.isic = []
                for i, f in enumerate(filter.split("+")):
                    if Isic.query.get(f):
                        self.isic.append(Isic.query.get(f))
                    else:
                        self.isic.append(Isic.query.get('c1010'))
                self.filter1 = "+".join([i.id for i in set(self.isic)])
            elif self.dataset == "secex":
                self.hs = []
                for i, f in enumerate(filter.split("+")):
                    if Hs.query.get(f):
                        self.hs.append(Hs.query.get(f))
                    else:
                        self.hs.append(Hs.query.get('178703'))
                self.filter1 = "+".join([h.id for h in set(self.hs)])
    
    def set_filter2(self, filter):
        if self.filter2 != "all":
            if self.dataset == "rais":
                self.cbo = []
                for i, f in enumerate(filter.split("+")):
                    if Cbo.query.get(f):
                        self.cbo.append(Cbo.query.get(f))
                    else:
                        self.cbo.append(Cbo.query.get('1210'))
                self.filter2 = "+".join([c.id for c in set(self.cbo)])
            elif self.dataset == "secex":
                self.wld = []
                for i, f in enumerate(filter.split("+")):
                    if Wld.query.get(f):
                        self.wld.append(Wld.query.get(f))
                    else:
                        self.wld.append(Wld.query.get('aschn'))
                self.filter2 = "+".join([w.id for w in set(self.wld)])
        
    '''Returns the URL for the specific build.'''
    def url(self, **kwargs):
        bras = []
        for b in self.bra:
            if b.id != "all" and b.distance > 0:
                bras.append(b.id+"."+b.distance)
            else:
                bras.append(b.id)
                
        bra_id = "+".join(bras)
        
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.app.type, 
                self.dataset, bra_id, self.filter1, self.filter2, self.output)
        return url

    '''Returns the data URL for the specific build. This URL will return the 
    data required for building a viz of this app.
    '''
    def data_url(self, **kwargs):
        print self.bra
        
        bras = []
        for b in self.bra:
            if b.id != "all" and b.distance > 0:
                bras.append(b.id+"."+b.distance)
            else:
                bras.append(b.id)
                
        bra = "+".join(bras)
        
        if self.app.type == "geo_map" and bra == "all":
            bra = "all.show.2"
        elif self.output == "bra":
            bra = bra + ".show.8"
            
        filter1 = self.filter1
        if filter1 == "all" or self.app.type == "rings":
            if self.output == "isic":
                filter1 = "show.5"
            elif self.output == "hs":
                filter1 = "show.6"
        
        filter2 = self.filter2
        if filter2 == "all" or self.app.type == "rings":
            if self.output == "cbo":
                filter2 = "show.4"
            elif self.output == "wld":
                filter2 = "show.5"

        data_url = '{0}/all/{1}/{2}/{3}/'.format(self.dataset, bra, 
            filter1, filter2)
        return data_url
    
    '''Returns the data table required for this build'''
    def data_table(self):
        from visual.rais.models import Ybi, Ybo, Yio, Yb_rais, Yi, Yo
        from visual.secex.models import Ybp, Ybw, Ypw, Yb_secex, Yp, Yw
        
        # raise Exception(self.output)
        if self.dataset == "rais":
            # raise Exception(self.bra[0], self.filter1, self.filter2, self.output)
            if self.bra[0].id == "all" and self.output != "bra":
                return Yio
            elif self.output == "isic" or (self.output == "bra" and self.filter2 == "all"):
                return Ybi
            elif self.output == "cbo" or (self.output == "bra" and self.filter1 == "all"):
                return Ybo
        elif self.dataset == "secex":
            if self.bra[0].id == "all" and self.output != "bra":
                return Ypw
            elif self.output == "hs" or (self.output == "bra" and self.filter2 == "all"):
                return Ybp
            elif self.output == "wld" or (self.output == "bra" and self.filter1 == "all"):
                return Ybw
            
            
            
            if self.filter1 == "all":
                return Ybw
            elif self.filter1 == "all":
                return Ybp
    
    '''Returns the english language title of this build.'''
    def title(self, **kwargs):
        lang = g.locale
        if "lang" in kwargs:
            lang = kwargs["lang"]
        
        title_lang = "title_en" if lang == "en" else "title_pt"
        name_lang = "name_en" if lang == "en" else "name_pt"
        
        title = getattr(self, title_lang)
        
        def get_article(attr, article):
            if attr.article_pt:
                if attr.gender_pt == "m":
                    if article == "em": new_article = "no"
                    if article == "de": new_article = "do" 
                    if article == "para": new_article = "para o" 
                elif attr.gender_pt == "f":
                    if article == "em": new_article = "na" 
                    if article == "de": new_article = "da"
                    if article == "para": new_article = "para a" 
                if attr.plural_pt:
                    new_article = new_article + "s"
                return new_article
            else:
                return article
        
        if title:
            if "<bra>" in title:
                bras = []
                for b in self.bra:
                    name = getattr(b, name_lang)
                    if b.id != "all" and b.distance > 0:
                        name = name + " ("+b.distance+"km)"
                    bras.append(name)
                title = title.replace("<bra>", " and ".join(bras))
                article_search = re.search('<bra_(\w+)>', title)
                if article_search:
                    title = title.replace(article_search.group(0), " and ".join([get_article(b, article_search.group(1)) for b in self.bra]))
            if "<isic>" in title:
                title = title.replace("<isic>", ", ".join([getattr(i, name_lang) for i in self.isic]))
                article_search = re.search('<isic_(\w+)>', title)
                if article_search:
                    title = title.replace(article_search.group(0), " , ".join([get_article(b, article_search.group(1)) for b in self.bra]))
            if "<hs>" in title:
                title = title.replace("<hs>", ", ".join([getattr(h, name_lang) for h in self.hs]))
                article_search = re.search('<hs_(\w+)>', title)
                if article_search:
                    title = title.replace(article_search.group(0), " , ".join([get_article(b, article_search.group(1)) for b in self.bra]))
            if "<cbo>" in title:
                title = title.replace("<cbo>", ", ".join([getattr(c, name_lang) for c in self.cbo]))
                article_search = re.search('<cbo_(\w+)>', title)
                if article_search:
                    title = title.replace(article_search.group(0), " , ".join([get_article(b, article_search.group(1)) for b in self.bra]))
            if "<wld>" in title:
                title = title.replace("<wld>", ", ".join([getattr(w, name_lang) for w in self.wld]))
                article_search = re.search('<wld_(\w+)>', title)
                if article_search:
                    title = title.replace(article_search.group(0), " , ".join([get_article(b, article_search.group(1)) for b in self.bra]))

        return title
            

    def serialize(self, **kwargs):
        
        auto_serialized = super(Build, self).serialize()
        
        auto_serialized["bra"] = [b.serialize() for b in self.bra]
        
        for i,b in enumerate(auto_serialized["bra"]):
            if b["id"] != "all" and self.bra[i].distance:
                b["distance"] = self.bra[i].distance
        
        if hasattr(self, "isic"):
            auto_serialized["isic"] = [i.serialize() for i in self.isic]
        if hasattr(self, "hs"):
            auto_serialized["hs"] = [h.serialize() for h in self.hs]
        if hasattr(self, "cbo"):
            auto_serialized["cbo"] = [c.serialize() for c in self.cbo]
        if hasattr(self, "wld"):
            auto_serialized["wld"] = [w.serialize() for w in self.wld]
        auto_serialized["title"] = self.title()
        auto_serialized["data_url"] = self.data_url()
        auto_serialized["url"] = self.url()
        auto_serialized["ui"] = [ui.serialize() for ui in self.ui.all()]
        auto_serialized["app"] = self.app.serialize()
        
        return auto_serialized

    def __repr__(self):
        return '<Build %s:%r: %s/%s/%s>' % (self.id, self.app.type, self.filter1, self.filter2, self.output)

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