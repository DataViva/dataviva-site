from flask import g
from visual import db
from visual.utils import AutoSerialize
from visual.attrs.models import Bra, Isic, Hs, Cbo, Wld
from visual.apps.models import Build

import ast, re

class Plan_Build(db.Model, AutoSerialize):

    __tablename__ = 'apps_plan_build'
    __public__ = ('plan_id', 'build_id', 'position', 'type', 'variables')
    
    plan_id = db.Column(db.Integer, primary_key = True)
    build_id = db.Column(db.Integer, primary_key = True)
    position = db.Column(db.Integer)
    type = db.Column(db.String(10))
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
        lang = g.locale
        if "lang" in kwargs:
            lang =  kwargs["lang"]

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
                and_joiner = " and " if lang == "en" else " e "
                title = title.replace("<bra>", and_joiner.join([getattr(b, name_lang) for b in self.bra]))
                article_search = re.search('<bra_(\w+)>', title)
                if article_search:
                    title = title.replace(article_search.group(0), and_joiner.join([get_article(b, article_search.group(1)) for b in self.bra]))
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