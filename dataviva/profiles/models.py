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
            q = setup["data"].query.filter(getattr(setup["data"], setup["id"]).in_(q)).group_by(getattr(setup["data"], setup["id"])).order_by(getattr(setup["data"], setup["column"]).desc()).limit(3)
            return [getattr(a, setup["id"]) for a in q.all()]
        return []

    def builds(self):

        secex_restricted = False
        if self.type == "bra":
            bra = self.attr

            # removes SECEX builds if not data, test with '4mg050305'
            if bra.id != "all":
                q = Ymb.query.filter(Ymb.bra_id == bra.id).first()
                secex_restricted = q

        else:
            bra = attrs.Wld.query.get("sabra")
            bra.id = "all"

        apps = self.build_list()

        build_ids = []
        for group in apps:
            for i, v in enumerate(group["builds"]):

                if not isinstance(v, list):
                    v = [v]

                for ii, a in enumerate(v):

                    if isinstance(a, int):
                        a = {"id": a}

                    if not a["id"] in build_ids:
                        build_ids.append(a["id"])

                    v[ii] = a

                group["builds"][i] = v

        build_ids = Build.query.filter(Build.id.in_(build_ids)).all()
        build_ids = {b.id: b for b in build_ids}

        position = 1
        for group in apps:
            for i, v in enumerate(group["builds"]):

                for ii, a in enumerate(v):

                    b = build_ids[a["id"]]

                    # removes SECEX builds if not data, test with '4mg050305'
                    if b.dataset == "secex" and secex_restricted == None:
                        v[ii] = None
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
                    b["titlelock"] = "title" in a
                    if b["titlelock"]:
                        b["slug"] = a["title"]
                    position += 1

                    v[ii] = b

                v = [b for b in v if b != None]
                group["builds"][i] = v if len(v) else None
            group["builds"] = [b for b in group["builds"] if b != None]

        apps = [g for g in apps if len(g["builds"]) > 0]
        return apps

    def __repr__(self):
        return "<{} profile for {}>".format(self.type.capitalize(), self.name())

class Bra(Profile):

    def build_list(self):
        apps = [
            {"builds": [91]},
            {"title": gettext("Exports by:"), "builds": [
                [
                    {"id":9, "params": {"size": "export_val"}},
                    {"id":25, "params": {"size": "export_val"}},
                    {"id":46, "params": {"size": "export_val"}}
                ],
                [
                    {"id":11, "params": {"size": "export_val"}},
                    {"id":27, "params": {"size": "export_val"}},
                    {"id":134, "params": {"size": "export_val"}}
                ]
            ]},
            {"title": gettext("Imports by:"), "builds": [
                [
                    {"id":9, "params": {"size": "import_val"}},
                    {"id":25, "params": {"size": "import_val"}},
                    {"id":46, "params": {"size": "import_val"}}
                ],
                [
                    {"id":11, "params": {"size": "import_val"}},
                    {"id":27, "params": {"size": "import_val"}},
                    {"id":134, "params": {"size": "import_val"}}
                ]
            ]},
            {"title": gettext("Employment by:"), "builds": [[1, 17, 140], [3, 19, 142]]},
            {"title": gettext("Wages by:"), "builds": [
                [
                    {"id": 1, "params": {"size": "wage"}},
                    {"id": 17, "params": {"size": "wage"}},
                    {"id": 140, "params": {"size": "wage"}}
                ],
                [
                    {"id": 3, "params": {"size": "wage"}},
                    {"id": 19, "params": {"size": "wage"}},
                    {"id": 142, "params": {"size": "wage"}}
                ]
            ]},
            {"title": gettext("Economic Opportunities:"), "builds": [35, 33]},
            {"title": gettext("Domestic Trade by:"), "builds": [128, 127]},
            {"title": gettext("University Enrollment by:"), "builds": [93, [95, 105, 115]]},
            {"title": gettext("Vocational Enrollment by:"), "builds": [[117, 120, 126]]},
            {"title": gettext("Basic Education by:"), "builds": [160]}
        ]
        if len(self.attr.id) < 9:
            for i, val in enumerate(["export_val", "import_val"]):
                exp_builds = []
                for b in [40,13,29]:
                    exp_builds.append({"id": b, "params": {"size": val}})
                apps[i+1]["builds"].append(exp_builds)
            apps[3]["builds"].append([36, 5, 21])
            apps[4]["builds"].append([
                {"id": 36, "params": {"color": "wage"}},
                {"id": 5, "params": {"size": "wage"}},
                {"id": 21, "params": {"size": "wage"}}
            ])
        return apps

class Hs(Profile):

    def build_list(self):

        apps = [
            {"builds": [148]},
            {"title": gettext("Exports by:"),
            "builds": [
                [
                    {"id": 12, "params": {"size": "export_val"}},
                    {"id": 28, "params": {"size": "export_val"}},
                    {"id": 135, "params": {"size": "export_val"}}
                ],
                [
                    {"id": 41, "params": {"size": "export_val"}},
                    {"id": 14, "params": {"size": "export_val"}},
                    {"id": 30, "params": {"size": "export_val"}}
                ]
            ]},
            {"title": gettext("Imports by:"),
            "builds": [
                [
                    {"id": 12, "params": {"size": "import_val"}},
                    {"id": 28, "params": {"size": "import_val"}},
                    {"id": 135, "params": {"size": "import_val"}}
                ],
                [
                    {"id": 41, "params": {"size": "import_val"}},
                    {"id": 14, "params": {"size": "import_val"}},
                    {"id": 30, "params": {"size": "import_val"}}
                ]
            ]}
        ]

        if len(self.attr.id) == 6:
            apps.append({
                "title": gettext("Economic Opportunities:"), "builds": [50]
            })

        industries = self.crosswalk_id()
        if len(industries):
            cross_apps = {"title": gettext("Common Industries by Occupation:"), "builds": []}
            for industry in industries:
                name = attrs.Cnae.query.get(industry).name()
                ind_builds = []
                for i in [4, 143, 51]:
                    ind_builds.append({"title": name, "id": i, "filter1": industry})
                cross_apps["builds"].append(ind_builds)
            apps.append(cross_apps)

        return apps

class Wld(Profile):

    def build_list(self):
        return [
            {"builds": [92]},
            {"title": gettext("Imports by:"),
            "builds": [
                [
                    {"id": 10, "params": {"size": "export_val"}},
                    {"id": 26, "params": {"y": "export_val"}},
                    {"id": 133, "params": {"y": "export_val"}}
                ],
                [
                    {"id": 15, "params": {"size": "export_val"}},
                    {"id": 31, "params": {"y": "export_val"}},
                    {"id": 42, "params": {"color": "export_val"}}
                ]
            ]},
            {"title": gettext("Exports by:"),
            "builds": [
                [
                    {"id": 10, "params": {"size": "import_val"}},
                    {"id": 26, "params": {"y": "import_val"}},
                    {"id": 133, "params": {"y": "import_val"}}
                ],
                [
                    {"id": 15, "params": {"size": "import_val"}},
                    {"id": 31, "params": {"y": "import_val"}},
                    {"id": 42, "params": {"color": "import_val"}}
                ]
            ]}
        ]

class Cnae(Profile):

    def build_list(self):

        apps = [
            {"title": gettext("Employment by:"),
            "builds": [
                [
                    {"id": 143, "params": {"size": "num_emp"}},
                    {"id": 4, "params": {"y": "num_emp"}},
                    {"id": 20, "params": {"y": "num_emp"}}
                ],
                [
                    {"id": 37, "params": {"size": "num_emp"}},
                    {"id": 6, "params": {"y": "num_emp"}},
                    {"id": 22, "params": {"color": "num_emp"}}
                ]
            ]},
            {"title": gettext("Average Wage by:"),
            "builds": [
                [
                    {"id": 143, "params": {"size": "wage_avg"}},
                    {"id": 20, "params": {"y": "wage_avg"}}
                ],
                [
                    {"id": 37, "params": {"size": "wage_avg"}},
                    {"id": 22, "params": {"color": "wage_avg"}}
                ]
            ]}
        ]

        if len(self.attr.id) == 6:
            apps.append({
                "title": gettext("Economic Opportunities:"), "builds": [51, 48]
            })

        products = self.crosswalk_id()
        if len(products):
            cross_apps = {"title": gettext("Common Products by Trade Partner:"), "builds": []}
            for product in products:
                name = attrs.Hs.query.get(product).name()
                prod_builds = []
                for i in [12,28,135]:
                    prod_builds.append({"title": name, "id": i, "filter1": product})
                cross_apps["builds"].append(prod_builds)
            apps.append(cross_apps)

        return apps

class Cbo(Profile):

    def build_list(self):
        apps = [
            {"title": gettext("Employment by:"),
            "builds": [
                [
                    {"id": 141, "params": {"y": "num_emp"}},
                    {"id": 2, "params": {"size": "num_emp"}},
                    {"id": 18, "params": {"y": "num_emp"}}
                ],
                [
                    {"id": 38, "params": {"color": "num_emp"}},
                    {"id": 7, "params": {"size": "num_emp"}},
                    {"id": 23, "params": {"y": "num_emp"}}
                ],
            ]},
            {"title": gettext("Average Wage by:"),
            "builds": [
                [
                    {"id": 141, "params": {"y": "wage_avg"}},
                    {"id": 18, "params": {"y": "wage_avg"}}
                ],
                [
                    {"id": 38, "params": {"color": "wage_avg"}},
                    {"id": 23, "params": {"y": "wage_avg"}}
                ],
            ]}
        ]

        if len(self.attr.id) == 4:
            apps.append({
                "title": gettext("Economic Opportunities:"), "builds": [49]
            })

        courses = self.crosswalk_id()
        if len(courses):
            cross_apps = {"title": gettext("Common Majors by University:"), "builds": []}
            for course in courses:
                name = attrs.Course_hedu.query.get(course).name()
                cross_apps["builds"].append({"title": name, "id": 94, "filter2": course, "params": {"color": "graduates_growth"}})
            apps.append(cross_apps)
        return apps

class University(Profile):

    def build_list(self):
        return [{"title": gettext("Enrollment by:"), "builds": [[96,106,116], 155, 151]}]

class Course_hedu(Profile):

    def build_list(self):
        apps = [{
            "title": gettext("Enrollment by:"),
            "builds": [{"id": 94, "params": {"y": "graduates_growth"}}, [110,108,99], 156, 152]
        }]

        occupations = self.crosswalk_id()
        if len(occupations):
            cross_apps = {"title": gettext("Common Occupations by Industry:"), "builds": []}
            for occupation in occupations:
                name = attrs.Cbo.query.get(occupation).name()
                occ_builds = []
                for i in [2,18,141]:
                    occ_builds.append({"title": name, "id": i, "filter2": occupation})
                cross_apps["builds"].append(occ_builds)
            apps.append(cross_apps)
        return apps

class Course_sc(Profile):

    def build_list(self):
        return [{"title": gettext("Vocational Enrollment by:"), "builds": [[124, 122, 119], 159]}]
