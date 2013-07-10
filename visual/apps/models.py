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
        
        bra = self.bra.id
        if self.filter1 == "all": filter1 = "all"
        else: filter1 = self.filter1.id
        if self.filter2 == "all": filter2 = "all"
        else: filter2 = self.filter2.id
        
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.app.viz_whiz, 
                self.dataset, bra, filter1, filter2, self.output)
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
        lang = "en"
        if "lang" in kwargs:
            lang =  kwargs["lang"]
        
        title_lang = "title_en" if lang == "en" else "title_pt"
        name_lang = "name_en" if lang == "en" else "name_pt"
        
        title = getattr(self, title_lang)
        
        if "<bra>" in title:
            title = title.replace("<bra>", getattr(self.bra, name_lang))
        if "<isic>" in title:
            title = title.replace("<isic>", getattr(self.filter1, name_lang))
        elif "<hs>" in title:
            title = title.replace("<hs>", getattr(self.filter1, name_lang))
        if "<cbo>" in title:
            title = title.replace("<cbo>", getattr(self.filter2, name_lang))
        elif "<wld>" in title:
            title = title.replace("<wld>", getattr(self.filter2, name_lang))
        
        return title
            

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