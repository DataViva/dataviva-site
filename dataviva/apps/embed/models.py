# -*- coding: utf-8 -*-
from flask import g
from dataviva import db, __year_range__
from dataviva.translations.dictionary import dictionary
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.utils.title_case import title_case
from dataviva.utils.title_format import title_format
from dataviva.api.attrs.models import Bra, Cnae, Hs, Cbo, Wld, University, Course_hedu, Course_sc

import ast, re, urllib

build_ui = db.Table('apps_build_ui',
         db.Column('build_id', db.Integer,db.ForeignKey('apps_build.id')),
         db.Column('ui_id', db.Integer,db.ForeignKey('apps_ui.id'))
)

class App(db.Model, AutoSerialize):

    __tablename__ = 'apps_app'

    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(20))
    name_en = db.Column(db.String(20))
    name_pt = db.Column(db.String(20))
    d3plus = db.Column(db.String(20))
    color = db.Column(db.String(7))

    def name(self):
        lang = getattr(g, "locale", "en")
        return getattr(self,"name_"+lang)

    def serialize(self, **kwargs):
        auto_serialized = super(App, self).serialize()
        del auto_serialized["name_en"]
        del auto_serialized["name_pt"]
        auto_serialized["name"] = self.name()
        return auto_serialized

class Build(db.Model, AutoSerialize):

    __tablename__ = 'apps_build'

    id = db.Column(db.Integer, primary_key = True)
    dataset = db.Column(db.String(20))
    bra = db.Column(db.String(20))
    filter1 = db.Column(db.String(20))
    filter2 = db.Column(db.String(20))
    output = db.Column(db.String(20))
    title_en = db.Column(db.String(120))
    title_pt = db.Column(db.String(120))
    slug_en = db.Column(db.String(60))
    slug_pt = db.Column(db.String(60))
    slug2_en = db.Column(db.String(80))
    slug2_pt = db.Column(db.String(80))
    app_id = db.Column(db.Integer, db.ForeignKey(App.id))

    ui = db.relationship('UI', secondary=build_ui,
            backref=db.backref('Builds'), lazy='dynamic')
    app = db.relationship('App',
            backref=db.backref('Builds', lazy='dynamic'))

    params = None

    def get_ui(self, ui_type):
        return self.ui.filter(UI.type == ui_type).first()

    # def brazil_allowed(self):
    #     return (self.app_id not in [6,8]) and ((self.app_id not in [4,5]) or self.dataset != "rais")

    def limit_bra(self, bra):
        if isinstance(bra, Wld):
            # if not self.brazil_allowed():
            #     return Bra.query.get("4mg")
            # else:
            bra.id = "all"
        return bra

    def set_bra(self, bra_id):

        if isinstance(bra_id, (Bra, Wld)):
            bra_id = self.limit_bra(bra_id)
            bra_id = [bra_id]
        elif isinstance(bra_id, (list)) and isinstance(bra_id[0], (Bra, Wld)):
            bra_id = [self.limit_bra(b) for b in bra_id]
        else:
            if bra_id == "bra":
                bra_id = "all"

            if "_" in self.bra and "_" not in bra_id:
                bra_id = bra_id + "_all"
            elif "_" not in self.bra and "_" in bra_id:
                bra_id = bra_id.split("_")[0]

            bra_id = bra_id.split("_")

        self.bra = []

        for i, b in enumerate(bra_id):
            if isinstance(b, (Bra, Wld)):
                # if b.id.startswith("4mgplr"):
                #     b.pr_ids = [pr.id for pr in b.pr.all()]
                # else:
                #     b.pr_ids = []
                self.bra.append(b)
            elif b == "all":
                self.bra.append(Wld.query.get("sabra"))
                self.bra[i].id = "all"
            else:
                if "." in b:
                    split = b.split(".")
                    b = split[0]
                    dist = split[1]
                else:
                    dist = 0
                state = b[:3]
                if self.output == "bra" and len(b) == 9 and dist == 0:
                    b = state
                    dist = 0
                self.bra.append(Bra.query.get(b))
                self.bra[i].distance = dist
                self.bra[i].neighbor_ids = [b.bra_id_dest for b in self.bra[i].get_neighbors(dist)]
                # if b.startswith("4mg"):
                #     self.bra[i].pr_ids = [b.id for b in self.bra[i].pr.all()]
                # else:
                #     self.bra[i].pr_ids = []

    def set_filter1(self, filter):
        if self.filter1 != "all":

            if self.dataset == "rais":
                name = "cnae"
                default = "r90019"
            elif self.dataset == "secex":
                name = "hs"
                default = "178703"
            elif self.dataset == "hedu":
                name = "university"
                default = "00575"

            items = []
            attr = globals()[name.capitalize()]

            if isinstance(filter, globals()[name.capitalize()]):
                items = [filter]
            elif isinstance(filter, (str, unicode)):
                for i, f in enumerate(filter.split("_")):
                    if attr.query.get(f):
                        items.append(attr.query.get(f))
                    else:
                        items.append(attr.query.get(default))
            else:
                items.append(attr.query.get(default))

            self.filter1 = "_".join([c.id for c in set(items)])
            setattr(self, name, items)

    def set_filter2(self, filter):
        if self.filter2 != "all":

            if self.dataset == "rais":
                name = "cbo"
                default = "2211"
            elif self.dataset == "secex":
                name = "wld"
                default = "aschn"
            elif self.dataset == "hedu":
                name = "course_hedu"
                default = "345A01"
            elif self.dataset == "sc":
                name = "course_sc"
                default = "13182"

            items = []
            attr = globals()[name.capitalize()]

            if isinstance(filter, globals()[name.capitalize()]):
                items = [filter]
            elif isinstance(filter, (str, unicode)):
                for i, f in enumerate(filter.split("_")):
                    if attr.query.get(f):
                        items.append(attr.query.get(f))
                    else:
                        items.append(attr.query.get(default))
            else:
                items.append(attr.query.get(default))

            self.filter2 = "_".join([c.id for c in set(items)])
            setattr(self, name, items)

    '''Returns the URL for the specific build.'''
    def url(self, **kwargs):

        fill = kwargs.get("fill", True)

        if fill:
            if isinstance(self.bra,(list,tuple)):
                bras = []
                for b in self.bra:
                    if b.id != "all" and b.distance > 0:
                        bras.append(b.id+"."+b.distance)
                    else:
                        bras.append(b.id)
                bra_id = "_".join(bras)
            else:
                bra_id = self.bra
            f1 = self.filter1
            f2 = self.filter2
        else:
            bra_id = self.bra
            if self.app.type == "compare":
                bra_id = "<bra>_<bra_1>"

            f1 = self.filter1
            if f1 != "all":
                if self.dataset == "rais":
                    f1 = "<cnae>"
                elif self.dataset == "secex":
                    f1 = "<hs>"
                elif self.dataset == "hedu":
                    f1 = "<university>"

            f2 = self.filter2
            if f2 != "all":
                if self.dataset == "rais":
                    f2 = "<cbo>"
                elif self.dataset == "secex":
                    f2 = "<wld>"
                elif self.dataset == "hedu":
                    f2 = "<course_hedu>"
                elif self.dataset == "sc":
                    f2 = "<course_sc>"

        if self.params:
            params = "?{}".format(urllib.urlencode(self.params))
        else:
            params = ""

        return "{}/{}/{}/{}/{}/{}/{}".format(self.app.type, self.dataset, bra_id, f1, f2, self.output, params)

    '''Returns the data URL for the specific build. This URL will return the
    data required for building a viz of this app.
    '''
    def data_url(self, **kwargs):

        bras = []
        if isinstance(self.bra,(list,tuple)):
            for b in self.bra:
                if b.id != "all" and b.distance > 0:
                    bras.append(b.id+"."+b.distance)
                else:
                    bras.append(b.id)
            bra = "_".join(bras)
        else:
            bra = "<bra>"

        if self.output == "bra" and self.dataset != "ei":
            if bra == "all":
                if self.app.type == "geo_map":
                    bra = "show.3"
                elif self.app.type == "bar":
                    bra = "show.1"
                else:
                    bra = "show.9"
            elif self.app.type == "bar":
                bra = "{}.show.{}".format(bra, len(bra))
            else:
                bra = bra + ".show.9"

        filter1 = self.filter1
        filter1_out = None

        depths = {
            "cnae": 6,
            "hs": 6,
            "university": 5,
            "school": 8
        }
        if self.output in depths:
            if self.app.type == "bar" and filter1 != "all":
                depth = len(filter1)
            else:
                depth = depths[self.output]
            filter1_out = "show.{}".format(depth)

        if filter1_out:
            if filter1 == "all":
                filter1 = filter1_out
            else:
                filter1 = "{}.{}".format(filter1, filter1_out)

        filter2 = self.filter2
        filter2_out = None

        depths = {
            "cbo": 4,
            "wld": 5,
            "course_sc": 5,
            "course_hedu": 6
        }
        if self.output in depths:
            if self.app.type == "bar" and filter2 != "all":
                depth = len(filter2)
            else:
                depth = depths[self.output]
            filter2_out = "show.{}".format(depth)

        if filter2_out:
            if filter2 == "all":
                filter2 = filter2_out
            else:
                filter2 = "{}.{}".format(filter2, filter2_out)

        if self.output in ("balance", "time", "type"):
            if bra != "all":
                bra = bra + ".show.{}".format(len(bra))
            elif filter1 != "all":
                filter1 = filter1 + ".show.{}".format(len(filter1))
            elif filter2 != "all":
                filter2 = filter2 + ".show.{}".format(len(filter2))
            else:
                bra = "show.1"
        elif self.output == "age":
            filter1 = "show.8"
            filter2 = "xx.show.5"
        elif self.output == "basic":
            filter2 = "xx.show.5"
        elif self.output == "adm":
            filter1 = "show.8"

        params = ""
        if self.output == "course_sc" and self.filter2 == "all":
            params = "?exclude=xx%"

        if self.dataset == "ei":
            if self.output == "bra":
                return "ei/all/show.9/{}/{}".format(bra, params)
            else:
                return "ei/all/{}/show.9/{}".format(bra, params)

        return "{}/all/{}/{}/{}/{}".format(self.dataset, bra, filter1, filter2, params)

    '''Returns the data table required for this build'''
    def data_table(self):
        from dataviva.api.rais.models import Ybi, Ybo, Yio, Yb_rais, Yi, Yo
        from dataviva.api.secex.models import Ymbp, Ymbw, Ympw, Ymb, Ymp, Ymw

        # raise Exception(self.output)
        if self.dataset == "rais":
            # raise Exception(self.bra[0], self.filter1, self.filter2, self.output)
            if self.bra[0].id == "all" and self.output != "bra":
                return Yio
            elif self.output == "cnae" or (self.output == "bra" and self.filter2 == "all"):
                return Ybi
            elif self.output == "cbo" or (self.output == "bra" and self.filter1 == "all"):
                return Ybo
        elif self.dataset == "secex":
            if self.bra[0].id == "all" and self.output != "bra":
                return Ympw
            elif self.output == "hs" or (self.output == "bra" and self.filter2 == "all"):
                return Ymbp
            elif self.output == "wld" or (self.output == "bra" and self.filter1 == "all"):
                return Ymbw

            if self.filter1 == "all":
                return Ymbw
            elif self.filter1 == "all":
                return Ymbp

    def format_text(self, title, kwargs):

        if kwargs.get("dumb") == True:
            return title

        lookup = dictionary()

        depth = kwargs.get("depth", None)
        year = kwargs.get("year", None)

        munic = lookup["bra_9"]
        munics = lookup["bra_9_plural"]

        if depth and u"bra_" in depth[0] and depth[0] != "bra_8":
            if munics in title:
                title = title.replace(munics,lookup["bra_{}_plural".format(depth[0])])
            if munic in title:
                title = title.replace(munic,lookup["bra_{}".format(depth[0])])

        if self.output == "bra" and isinstance(self.bra,(list,tuple)) and self.bra[0].id == "all":
             title = title.replace(munics,lookup["bra_3_plural"])
             title = title.replace(munic,lookup["bra_3"])

        flow = kwargs.get("size", None)
        if not flow:
            flow = kwargs.get("y", None)
        if not flow:
            flow = kwargs.get("axes", None)
        if not flow:
            flow = "export_val"

        flow = "{}s".format(flow[:-4])

        impexp = u"{}/{}".format(lookup["import_val"],lookup["export_val"])
        if impexp in title and flow in lookup:
            title = title.replace(impexp, lookup[flow])


        impexp = u"{}/{}".format(lookup["origin"],lookup["destination"])
        if impexp in title:
            if flow == "imports":
                rep = lookup["origins"]
            else:
                rep = lookup["destination"]
            title = title.replace(impexp, rep)

        impexp = u"{}/{}".format(lookup["origins"],lookup["destinations"])
        if impexp in title:
            if flow == "imports":
                rep = lookup["origins"]
            else:
                rep = lookup["destination"]
            title = title.replace(impexp, rep)

        if not year:
            if self.app_id in [2,9]:
                year = "_".join(__year_range__[self.dataset])
            else:
                year = __year_range__[self.dataset][1]

        monthly = self.dataset != "secex" or self.app_id in [2,9]

        def format_date(d):
            if "-" in d:
                y, m = d.split("-")
                if monthly:
                    if m == "0":
                        m = "1"
                    d = "{} {}".format(lookup["month_{}".format(m)], y)
                else:
                    d = y
            return d

        year = [format_date(y) for y in year.split("_")]

        title += " ({0})".format("-".join(year))

        return title

    def slug(self, **kwargs):

        slug = getattr(self, "slug_{}".format(g.locale))
        slug = self.format_text(slug, kwargs)

        return slug

    def slug2(self):
        return getattr(self, "slug2_{}".format(g.locale))


    '''Returns the english language title of this build.'''
    def title(self, **kwargs):

        title = getattr(self, "title_{}".format(g.locale))
        title = self.format_text(title, kwargs)

        if title:
            for f in ["bra", "cnae", "hs", "cbo", "wld", "university", "course_hedu", "course_sc"]:
                if hasattr(self, f):
                    attr = getattr(self, f)
                    if not isinstance(attr, (unicode, str)):
                        title = title_format(title, attr)

        return title

    def json(self, **kwargs):
        return {
            "app": self.app.serialize(),
            "dataset": self.dataset,
            "id": int(self.id),
            "slug": self.slug(**kwargs),
            "slug2": self.slug2(),
            "title": self.title(**kwargs),
            "url": self.url(**kwargs)
        }


    def serialize(self, **kwargs):

        auto_serialized = super(Build, self).serialize()

        if isinstance(self.bra,(list,tuple)):
            auto_serialized["bra"] = [b.serialize() for b in self.bra]
            for i,b in enumerate(auto_serialized["bra"]):
                if b["id"] != "all" and self.bra[i].distance:
                    b["distance"] = self.bra[i].distance
                    b["neighbor_ids"] = self.bra[i].neighbor_ids
                # elif b["id"].startswith("4mg"):
                #     b["pr_ids"] = self.bra[i].pr_ids

        for f in ["cnae", "cbo", "hs", "wld", "university", "course_hedu", "course_sc"]:
            if hasattr(self, f):
                auto_serialized[f] = [i.serialize() for i in getattr(self, f)]

        del auto_serialized["title_en"]
        del auto_serialized["title_pt"]
        auto_serialized["id"] = int(self.id)
        auto_serialized["title"] = self.title()
        auto_serialized["slug"] = self.slug()
        auto_serialized["data_url"] = self.data_url()
        auto_serialized["url"] = self.url()
        auto_serialized["ui"] = [ui.serialize() for ui in self.ui.all()]
        auto_serialized["app"] = self.app.serialize()
        if self.dataset == "ei":
            auto_serialized["output_attr"] = "bra"
        elif self.output == "age" or self.output == "basic":
            auto_serialized["output_attr"] = "course_sc"
        elif self.output == "adm":
            auto_serialized["output_attr"] = "school"
        else:
            auto_serialized["output_attr"] = self.output

        return auto_serialized

    def __repr__(self):
        return '<Build %s:%r: %s/%s/%s>' % (self.id, self.app.type, self.filter1, self.filter2, self.output)

class UI(db.Model, AutoSerialize):

    __tablename__ = 'apps_ui'

    id = db.Column(db.Integer, db.ForeignKey(Build.id), primary_key = True)
    type = db.Column(db.String(20))
    values = db.Column(db.String(255))

    def serialize(self, **kwargs):
        auto_serialized = super(UI, self).serialize()
        auto_serialized["values"] = ast.literal_eval(self.values)
        return auto_serialized

    def __repr__(self):
        return '<Build %r: %r>' % (self.type, self.values)

class Crosswalk_oc(db.Model):
    __tablename__ = 'crosswalk_oc'

    cbo_id = db.Column(db.String(4), db.ForeignKey(Cbo.id), primary_key = True)
    course_hedu_id = db.Column(db.String(6), db.ForeignKey(Course_hedu.id), primary_key = True)

    def get_id(self, dataset):
        if dataset == "rais":
            return self.course_hedu_id
        return self.cbo_id

class Crosswalk_pi(db.Model):
    __tablename__ = 'crosswalk_pi'

    hs_id = db.Column(db.String(6), primary_key = True)
    cnae_id = db.Column(db.String(5), primary_key = True)

    def get_id(self, dataset):
        if dataset == "rais":
            return self.hs_id
        return self.cnae_id
