from flask import g
from visual import db
from visual.utils import AutoSerialize
from visual.attrs.models import Bra, Isic, Hs, Cbo, Wld
from visual.apps.models import Build

import ast

class Plan_Build(db.Model, AutoSerialize):

    __tablename__ = 'apps_plan_build'
    __public__ = ('plan_id', 'build_id', 'position', 'variables')
    
    plan_id = db.Column(db.Integer, primary_key = True)
    build_id = db.Column(db.Integer, primary_key = True)
    position = db.Column(db.Integer)
    variables = db.Column(db.String(120))
    
    build = db.relationship("Build",
            primaryjoin= "Build.id==Plan_Build.build_id",
            foreign_keys=[Build.id], backref = 'plan_build', lazy = 'dynamic')
    

class Plan(db.Model, AutoSerialize):

    __tablename__ = 'apps_plan'
    
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(20))
    category_type = db.Column(db.String(20))
    option = db.Column(db.String(20))
    option_type = db.Column(db.String(20))
    option_id = db.Column(db.String(20))
    title_en = db.Column(db.String(120))
    title_pt = db.Column(db.String(120))
            
    builds = db.relationship("Plan_Build",
            primaryjoin= "Plan.id==Plan_Build.plan_id",
            foreign_keys=[Plan_Build.plan_id], backref = 'plan_build', lazy = 'dynamic')
         
    '''Returns the english language title of this plan.'''
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
        
    def set_attr(self, id, type):
        if type == "bra":
            self.bra = []
            for i, f in enumerate(id.split("+")):
                if f == "all":
                    self.bra.append(Wld.query.get("sabra"))
                    self.bra[i].id = "all"
                else:
                    self.bra.append(Bra.query.get(f))

            for pb in self.builds.all():
                pb.build.all()[0].set_bra(id)
                
        elif type == "cbo":
            self.cbo = []
            for i, f in enumerate(id.split("+")):
                self.cbo.append(Cbo.query.get(f))

            for pb in self.builds.all():
                pb.build.all()[0].set_filter2(f)
                
        elif type == "isic":
            self.isic = []
            for i, f in enumerate(id.split("+")):
                self.isic.append(Isic.query.get(f))

            for pb in self.builds.all():
                pb.build.all()[0].set_filter1(f)
                
        elif type == "wld":
            self.wld = []
            for i, f in enumerate(id.split("+")):
                self.wld.append(Wld.query.get(f))

            for pb in self.builds.all():
                pb.build.all()[0].set_filter2(f)
                
        elif type == "hs":
            self.hs = []
            for i, f in enumerate(id.split("+")):
                self.hs.append(Hs.query.get(f))

            for pb in self.builds.all():
                pb.build.all()[0].set_filter1(f)

    def __repr__(self):
        return '<Plan "%s": %s>' % (self.id,self.builds.all())