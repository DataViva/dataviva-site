from flask import g
from visual import db
from visual.utils import AutoSerialize
from visual.attrs.models import Bra, Isic, Hs, Cbo, Wld

import ast

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
        self.bra = []
        if bra_id == "all":
            self.bra.append(Wld.query.get("sabra"))
            self.bra[0].id = "all"
            self.bra[0].icon = "/static/img/icons/wld/wld_sabra.png"
        else:
            for i, b in enumerate(bra_id.split("+")):
                self.bra.append(Bra.query.get(b))
                self.bra[i].icon = "/static/img/icons/bra/bra_{0}.png".format(b[:2])

    def set_filter1(self, filter):
        if self.filter1 == "all":
            self.filter1 = "all"
        elif self.dataset == "rais":
            self.isic = []
            for i, f in enumerate(filter.split("+")):
                if Isic.query.get(f):
                    self.isic.append(Isic.query.get(f))
                else:
                    self.isic.append(Isic.query.get('c1410'))
        elif self.dataset == "secex":
            self.hs = []
            for i, f in enumerate(filter.split("+")):
                if Hs.query.get(f):
                    self.hs.append(Hs.query.get(f))
                else:
                    self.hs.append(Hs.query.get('178703'))
        self.filter1 = filter
    
    def set_filter2(self, filter):
        if self.filter2 == "all":
            self.filter2 = "all"
        elif self.dataset == "rais":
            self.cbo = []
            for i, f in enumerate(filter.split("+")):
                if Cbo.query.get(f):
                    self.cbo.append(Cbo.query.get(f))
                else:
                    self.cbo.append(Cbo.query.get('1210'))
        elif self.dataset == "secex":
            self.wld = []
            for i, f in enumerate(filter.split("+")):
                if Wld.query.get(f):
                    self.wld.append(Wld.query.get(f))
                else:
                    self.wld.append(Wld.query.get('aschn'))
        self.filter2 = filter
        
    '''Returns the URL for the specific build.'''
    def url(self, **kwargs):
        
        # bra = self.bra.id
        # if self.filter1 == "all": filter1 = "all"
        # else: filter1 = self.filter1.id
        # if self.filter2 == "all": filter2 = "all"
        # else: filter2 = self.filter2.id
        bra_id = "+".join([b.id for b in self.bra])
        
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.app.viz_whiz, 
                self.dataset, bra_id, self.filter1, self.filter2, self.output)
        return url

    '''Returns the data URL for the specific build. This URL will return the 
    data required for building a viz of this app.
    '''
    def data_url(self, **kwargs):
        # filters = self.get_bra_and_filters(**kwargs)
        
        # bra = self.bra.id
        bra = "+".join([b.id for b in self.bra])
        if self.output == "bra":
            bra = bra + ".8"
            
        filter1 = self.filter1
        if filter1 == "all":
            if self.output == "isic":
                filter1 = "show.5"
            elif self.output == "hs":
                filter1 = "show.6"
        
        filter2 = self.filter2
        if filter2 == "all":
            if self.output == "cbo":
                filter2 = "show.4"
            elif self.output == "wld":
                filter2 = "show.5"

        # filter2 = "all" if self.filter2 == "all" else self.filter2.id
        # filter2 = "show" if self.output == "cbo" or self.output == "wld" else filter2

        data_url = '{0}/all/{1}/{2}/{3}/'.format(self.dataset, bra, 
            filter1, filter2)
        return data_url
    
    '''Returns the english language title of this build.'''
    def title(self, **kwargs):
        lang = "en"
        if "lang" in kwargs:
            lang =  kwargs["lang"]
        
        title_lang = "title_en" if lang == "en" else "title_pt"
        name_lang = "name_en" if lang == "en" else "name_pt"
        
        title = getattr(self, title_lang)
        
        if "<bra>" in title:
            title = title.replace("<bra>", ", ".join([getattr(b, name_lang) for b in self.bra]))
        if "<isic>" in title:
            title = title.replace("<isic>", ", ".join([getattr(i, name_lang) for i in self.isic]))
        if "<hs>" in title:
            title = title.replace("<hs>", ", ".join([getattr(h, name_lang) for h in self.hs]))
        if "<cbo>" in title:
            title = title.replace("<cbo>", ", ".join([getattr(c, name_lang) for c in self.cbo]))
        if "<wld>" in title:
            title = title.replace("<wld>", ", ".join([getattr(w, name_lang) for w in self.wld]))

        return title
            

    def serialize(self, **kwargs):
        auto_serialized = super(Build, self).serialize()

        auto_serialized["bra"] = [b.serialize() for b in self.bra]
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
        return '<Build %r/%r/%r>' % (self.filter1, self.filter2, self.output)

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