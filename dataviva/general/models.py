from flask import g
from datetime import datetime
from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.utils.title_case import title_case
from dataviva.attrs.models import Bra, Cnae, Hs, Cbo, Wld
from dataviva.apps.models import Build

import ast, re, string, random

class Plan_Build(db.Model, AutoSerialize):

    __tablename__ = 'apps_plan_build'
    plan_id = db.Column(db.Integer, primary_key = True)
    position = db.Column(db.Integer, primary_key = True)
    build_id = db.Column(db.Integer, primary_key = True)
    variables = db.Column(db.String(120))

    build = db.relationship("Build",
            primaryjoin= "Build.id==Plan_Build.build_id",
            foreign_keys=[Build.id], backref = 'plan_build', lazy = 'dynamic')

class Plan_Title(db.Model, AutoSerialize):

    __tablename__ = 'apps_plan_title'
    id = db.Column(db.Integer, primary_key = True)
    name_en = db.Column(db.String(120))
    name_pt = db.Column(db.String(120))


class Plan(db.Model, AutoSerialize):

    __tablename__ = 'apps_plan'

    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(20))
    category_type = db.Column(db.String(20))
    option = db.Column(db.String(20))
    option_type = db.Column(db.String(20))
    option_id = db.Column(db.String(20))
    title_id = db.Column(db.Integer)

    builds = db.relationship("Plan_Build",
            primaryjoin= "Plan.id==Plan_Build.plan_id",
            foreign_keys=[Plan_Build.plan_id], backref = 'plan_build', lazy = 'dynamic')

    '''Returns the english language title of this plan.'''
    def title(self, **kwargs):
        lang = g.locale
        if "lang" in kwargs:
            lang =  kwargs["lang"]

        name_lang = "name_en" if lang == "en" else "name_pt"

        title = getattr(Plan_Title.query.get(self.title_id),name_lang)

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
            variables = ["bra","cnae","hs","cbo","wld"]
            and_joiner = " and " if lang == "en" else " e "
            for var in enumerate(variables):
                filter = var[1]
                if "<{0}>".format(filter) in title:
                    title = title.replace("<{0}>".format(filter), and_joiner.join([getattr(b, name_lang) for b in getattr(self,filter)]))
                    article_search = re.search("<{0}_(\w+)>".format(filter), title)
                    if article_search:
                        title = title.replace(article_search.group(0), and_joiner.join([get_article(b, article_search.group(1)) for b in getattr(self,filter)]))

        return title_case(title)

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

        elif type == "cnae":
            self.cnae = []
            for i, f in enumerate(id.split("+")):
                self.cnae.append(Cnae.query.get(f))

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

class Short(db.Model):

    __tablename__ = 'apps_short'

    slug = db.Column(db.String(30), unique=True, primary_key=True)
    long_url = db.Column(db.String(255), unique=True)
    created = db.Column(db.DateTime, default=datetime.now)
    clicks = db.Column(db.Integer, default=0)

    @staticmethod
    def make_unique_slug(long_url):

        # Helper to generate random URL string
        # Thx EJF: https://github.com/ericjohnf/urlshort
        def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for x in range(size))

        # test if it already exists
        short = Short.query.filter_by(long_url = long_url).first()
        if short:
            return short.slug
        else:
            while True:
                new_slug = id_generator()
                if Short.query.filter_by(slug = new_slug).first() == None:
                    break
            return new_slug

    def __repr__(self):
        return "<ShortURL: '%s'>" % self.long_url
