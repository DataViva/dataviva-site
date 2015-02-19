# -*- coding: utf-8 -*-
from abc import ABCMeta
from urllib import urlencode as param
from flask.ext.babel import gettext

from dataviva.attrs import models as attrs
from dataviva.apps.models import Build, Crosswalk_oc, Crosswalk_pi
from dataviva.secex.models import Ymb, Ymp
from dataviva.rais.models import Yo, Yi
from dataviva.hedu.models import Yc_hedu

crosswalk_dict = {
    "cbo": {
        "table": Crosswalk_oc,
        "data": Yc_hedu,
        "column": "students",
        "id": "course_hedu_id"
    },
    "course_hedu": {
        "table": Crosswalk_oc,
        "data": Yo,
        "column": "num_emp",
        "id": "cbo_id"
    },
    "hs": {
        "table": Crosswalk_pi,
        "data": Yi,
        "column": "num_emp",
        "id": "cnae_id"
    },
    "cnae": {
        "table": Crosswalk_pi,
        "data": Ymp,
        "column": "export_val",
        "id": "hs_id"
    }
}

class Profile(object):

    __metaclass__ = ABCMeta

    def __init__(self, type, id):
        self.type = type
        attr = getattr(attrs, type.capitalize())
        if isinstance(id, attr):
            self.attr = id
        else:
            self.attr = attr.query.get_or_404(id)

    def name(self):
        return self.attr.name()

    def crosswalk_id(self):
        setup = crosswalk_dict[self.type]
        q = setup["table"].query.filter(getattr(setup["table"], "{}_id".format(self.type)) == self.attr.id).all()
        if len(q) > 0:
            q = [getattr(a, setup["id"]) for a in q]
            q = setup["data"].query.filter(getattr(setup["data"], setup["id"]).in_(q)).order_by(getattr(setup["data"], setup["column"]).desc())
            return getattr(q.first(), setup["id"])
        return None

    def builds(self):

        if self.type == "bra":
            bra = self.attr
        else:
            bra = attrs.Wld.query.get("sabra")
            bra.id = "all"

        apps = self.build_list()

        secex_restricted = None
        position = 1
        for group in apps:
            for i, a in enumerate(group["builds"]):

                if isinstance(a, (int)):
                    a = {"id": a}

                b = Build.query.get_or_404(a["id"])

                # removes SECEX builds if not data, test with '4mg050305'
                if b.dataset == "secex" and bra.id != "all":
                    if secex_restricted == None:
                        q = Ymb.query.filter(Ymb.bra_id == bra.id).all()
                        secex_restricted = len(q) == 0
                    if secex_restricted == True:
                        group["builds"][i] = None
                        continue

                b.set_bra(bra)

                if "filter1" in a:
                    b.set_filter1(a["filter1"])
                elif self.type in ["cnae","hs","university","school"]:
                    b.set_filter1(self.attr)
                if "filter2" in a:
                    b.set_filter2(a["filter2"])
                elif self.type in ["cbo","wld","course_hedu","course_sc"]:
                    b.set_filter2(self.attr)

                if "params" in a:
                    b = b.json(**a["params"])
                    b["url"] += "?{}".format(param(a["params"]))
                else:
                    b = b.json()

                b["position"] = position
                position += 1

                group["builds"][i] = b
            group["builds"] = [b for b in group["builds"] if b != None]

        apps = [g for g in apps if len(g["builds"]) > 0]
        return apps

    def __repr__(self):
        return "<{} profile for {}>".format(self.type.capitalize(), self.name())

class Bra(Profile):

    def build_list(self):
        apps = [
            {"title": gettext("International Trade"), "builds":
                [91, {"id":9, "params": {"size": "export_val"}},
                {"id":9, "params": {"size": "import_val"}},
                {"id":11, "params": {"size": "export_val"}},
                {"id":11, "params": {"size": "import_val"}}, 35]
            },
            {"title": gettext("Employment"), "builds": [17, 19, 33]},
            {"title": gettext("Domestic Trade"), "builds": [128, 127]},
            {"title": gettext("Higher Education"), "builds": [93, 105]},
            {"title": gettext("School Census"), "builds": [120]}
        ]
        if len(self.attr.id) < 9:
            apps[0]["builds"].insert(5, {"id": 13, "params": {"size": "export_val"}})
            apps[0]["builds"].insert(6, {"id": 13, "params": {"size": "import_val"}})
            apps[1]["builds"].insert(2, 5)
        return apps

class Hs(Profile):

    def build_list(self):
        apps = [{
            "title": gettext("Industrial Activity"),
            "builds": [148, 12, 137, 50]
        }]
        industry = self.crosswalk_id()
        if industry:
            apps.append({
                "title": gettext("Most Common Product"),
                "builds": [{"id": 4, "filter1": industry}, {"id": 48, "filter1": industry}]
            })
        return apps

class Wld(Profile):

    def build_list(self):
        apps = [{
            "title": gettext("International Trade"),
            "builds": [92, 10, 138]
        }]
        return apps

class Cnae(Profile):

    def build_list(self):
        apps = [{
            "title": gettext("Industrial Activity"),
            "builds": [{"id": 143, "params": {"y": "wage_avg"}},
            {"id": 22, "params": {"y": "wage_avg"}}, 4, 48]
        }]
        product = self.crosswalk_id()
        if product:
            apps.append({
                "title": gettext("Most Common Product"),
                "builds": [{"id": 12, "filter1": product}, {"id": 50, "filter1": product}]
            })
        return apps

class Cbo(Profile):

    def build_list(self):
        apps = [{
            "title": gettext("Employment"),
            "builds": [{"id": 141, "params": {"y": "wage_avg"}},
            {"id": 23, "params": {"y": "wage_avg"}}, 2, 49]
        }]
        course = self.crosswalk_id()
        if course:
            apps.append({
                "title": gettext("Most Common Major"),
                "builds": [{"id": 94, "filter2": course, "params": {"color": "graduates_growth"}}]
            })
        return apps

class University(Profile):

    def build_list(self):
        return [{"builds": [96, 116, 155, 151]}]

class Course_hedu(Profile):

    def build_list(self):
        apps = [{
            "title": gettext("Enrollment"),
            "builds": [156, 108, {"id": 94, "params": {"y": "graduates_growth"}}, 152]
        }]
        occupation = self.crosswalk_id()
        if occupation:
            apps.append({
                "title": gettext("Most Common Occupation"),
                "builds": [{"id": 49, "filter2": occupation}, {"id": 2, "filter2": occupation}]
            })
        return apps

class Course_sc(Profile):

    def build_list(self):
        return [{"builds": [119, 124, 159]}]
