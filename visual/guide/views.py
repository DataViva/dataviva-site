from flask import Blueprint, request, render_template, g, url_for
from sqlalchemy import func
from datetime import datetime

from visual import db
from visual.attrs import models as attrs
from visual.rais import models as rais
from visual.secex import models as secex

mod = Blueprint('guide', __name__, url_prefix='/guide')

@mod.before_request
def before_request():
    g.page_type = mod.name
    
    g.sabrina = {}
    g.sabrina["outfit"] = "casual"
    g.sabrina["face"] = "smile"
    g.sabrina["hat"] = None
    
    g.path = request.path

###############################
# Final Guide Page Views
# ---------------------------
@mod.route('/industry/<ind_id>/workforce/')
def guide_industry_workforce(ind_id = None):
    g.page_type = "plan"
    
    names = get_names({ "bra_id": "all", "ind_id": ind_id })
    
    title = u"What kind of workers are employed in {ind_id}?".format(**names)
    outfit = "worker"
    
    apps = app_obj(
        [
            { "app_name": "bubbles", "isic_id": ind_id },
            { "app_name": "stacked", "isic_id": ind_id, "output": "cbo" },
            { "app_name": "tree_map", "isic_id": ind_id, "output": "cbo" }
        ],names
    )
    
    recs = None
    
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)

@mod.route('/industry/<ind_id>/potential/<bra_id>/')
def guide_industry_potential(ind_id = None, bra_id = None):
    g.page_type = "plan"
    
    names = get_names({ "bra_id": bra_id, "ind_id": ind_id })
    
    if len(bra_id) == 8:
        title = u"What is the potential for {ind_id} in {bra_id}?".format(**names)
        recs = None
    else:
        title = u"What are some potential locations for {ind_id} in {bra_id}?".format(**names)
        recs = rec_list({ "bra_id": bra_id, "ind_id": ind_id },"bra",["growth_pct_total","rca_min","rca_max"]);
    outfit = "worker"
    
    if len(ind_id) in [1,5]:
        apps = app_obj(
            [
                { "app_name": "geo_map", "bra_id": bra_id, "isic_id": ind_id },
                { "app_name": "bubbles", "bra_id": bra_id, "isic_id": ind_id },
                { "app_name": "network", "bra_id": bra_id, "output": "isic" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "isic" },
                { "app_name": "rings", "bra_id": bra_id, "isic_id": ind_id }
            ],names
        )
    else:
        apps = app_obj(
            [
                { "app_name": "geo_map", "bra_id": bra_id, "hs_id": ind_id },
                { "app_name": "tree_map", "bra_id": bra_id, "hs_id": ind_id, "output": "wld" },
                { "app_name": "network", "bra_id": bra_id, "output": "hs" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "isic" },
                { "app_name": "rings", "bra_id": bra_id, "hs_id": ind_id }
            ],names
        )
        
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)

@mod.route('/industry/<ind_id>/diversification/')
def guide_industry_diversification(ind_id = None):
    g.page_type = "plan"
    
    names = get_names({ "bra_id": "all", "ind_id": ind_id })
    
    title = u"What are some diversification options for {ind_id}?".format(**names)
    outfit = "worker"
    
    if len(ind_id) in [1,5]:
        apps = app_obj(
            [
                { "app_name": "rings", "isic_id": ind_id },
                { "app_name": "stacked", "output": "isic" },
                { "app_name": "bubbles", "isic_id": ind_id }
            ],names
        )
    else:
        apps = app_obj(
            [
                { "app_name": "rings", "hs_id": ind_id },
                { "app_name": "stacked", "output": "hs" },
                { "app_name": "tree_map", "hs_id": ind_id, "output": "wld" }
            ],names
        )
    
    recs = False
    
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)

@mod.route('/industry/<ind_id>/location/<bra_id>/')
@mod.route('/location/<bra_id>/attract/<ind_id>/')
def guide_industry_location(bra_id = None, ind_id = None):
    g.page_type = "plan"
    
    names = get_names({ "bra_id": bra_id, "ind_id": ind_id })
    outfit = "worker"
    
    if request.environ['PATH_INFO'].split("/")[2] == "industry":
        title = u"What is the potential of {ind_id} in {bra_id}?".format(**names)
    else:
        title = u"How can I attract {ind_id} to {bra_id}?".format(**names)
    
    if len(ind_id) in [1,5]:
        apps = app_obj(
            [
                { "app_name": "bubbles", "bra_id": bra_id, "isic_id": ind_id },
                { "app_name": "rings", "bra_id": bra_id, "isic_id": ind_id },
                { "app_name": "tree_map", "bra_id": bra_id, "isic_id": ind_id, "output": "bra" },
                { "app_name": "geo_map", "bra_id": bra_id[:2], "isic_id": ind_id },
                { "app_name": "tree_map", "bra_id": bra_id, "output": "isic" }
            ],names
        )
    else:
        apps = app_obj(
            [
                { "app_name": "rings", "bra_id": bra_id, "hs_id": ind_id },
                { "app_name": "tree_map", "bra_id": bra_id, "hs_id": ind_id, "output": "bra" },
                { "app_name": "tree_map", "bra_id": bra_id, "hs_id": ind_id, "output": "wld" },
                { "app_name": "geo_map", "bra_id": bra_id[:2], "hs_id": ind_id },
                { "app_name": "tree_map", "bra_id": bra_id, "output": "hs" }
            ],names
        )
    
    if len(bra_id) == 8:
        recs = None
    else:
        recs = rec_list({ "bra_id": bra_id, "ind_id": ind_id },"bra",["growth_pct_total","rca_min","rca_max"]);
        
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)

@mod.route('/industry/<ind_id>/destinations/')
def guide_industry_destinations(ind_id = None):
    g.page_type = "plan"
    
    names = get_names({ "bra_id": "all", "ind_id": ind_id })
    
    title = u"What are the commercial destinations for {ind_id}?".format(**names)
    outfit = "worker"
    path = ["industry",str(ind_id),"destinations"]
    
    apps = app_obj(
        [
            { "app_name": "tree_map", "hs_id": ind_id, "output": "wld" },
            { "app_name": "geo_map", "hs_id": ind_id },
            { "app_name": "tree_map", "hs_id": ind_id, "output": "bra" },
            { "app_name": "stacked", "hs_id": ind_id, "output": "wld" }
        ],names
    )
    
    recs = False
    
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)

@mod.route('/location/<bra_id>/workforce/')
def guide_location_workforce(bra_id = None):
    g.page_type = "plan"
    
    names = get_names({ "bra_id": bra_id })
    
    title = u"What is the available workforce for {bra_id}?".format(**names)
    outfit = "travel"
    path = ["location",str(bra_id),"workforce"]
    
    apps = app_obj(
        [
            { "app_name": "stacked", "bra_id": bra_id, "output": "cbo" },
            { "app_name": "tree_map", "bra_id": bra_id, "output": "cbo" },
            { "app_name": "tree_map", "bra_id": bra_id, "output": "isic" }
        ],names
    )
    
    recs = False
    
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)

@mod.route('/location/<bra_id>/industry/<ind_type>/')
def guide_location_industry(bra_id = None, ind_type = None):
    g.page_type = "plan"
    
    names = get_names({ "bra_id": bra_id })
    outfit = "travel"
    
    if ind_type == "industries":
        title = u"What local industries are present in {bra_id}?".format(**names)
        apps = app_obj(
            [
                { "app_name": "tree_map", "bra_id": bra_id, "output": "isic" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "isic" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "cbo" }
            ],names
        )
    else:
        title = u"What products are exported from {bra_id}?".format(**names)
        apps = app_obj(
            [
                { "app_name": "tree_map", "bra_id": bra_id, "output": "hs" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "hs" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "cbo" }
            ],names
        )
    
    recs = None
    
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)

@mod.route('/location/<bra_id>/growth/<ind_type>/')
def guide_location_growth(bra_id = None, ind_type = None):
    g.page_type = "plan"
    
    names = get_names({ "bra_id": bra_id })
    outfit = "travel"
    
    if ind_type == "industries":
        title = u"What are the growing local industries in {bra_id}?".format(**names)
        apps = app_obj(
            [
                { "app_name": "tree_map", "bra_id": bra_id, "output": "isic" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "isic" },
                { "app_name": "tree_map", "bra_id": bra_id, "output": "hs" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "hs" }
            ],names
        )
    else:
        title = u"What are the growing product exports in {bra_id}?".format(**names)
        apps = app_obj(
            [
                { "app_name": "tree_map", "bra_id": bra_id, "output": "hs" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "hs" },
                { "app_name": "tree_map", "bra_id": bra_id, "output": "isic" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "isic" }
            ],names
        )
    
    recs = False
    
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)

@mod.route('/location/<bra_id>/shrink/<ind_type>/')
def guide_location_shrink(bra_id = None, ind_type = None):
    g.page_type = "plan"
    
    names = get_names({ "bra_id": bra_id })
    outfit = "travel"
    
    if ind_type == "industries":
        title = u"What are the shrinking local industries in {bra_id}?".format(**names)
        apps = app_obj(
            [
                { "app_name": "tree_map", "bra_id": bra_id, "output": "isic" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "isic" },
                { "app_name": "tree_map", "bra_id": bra_id, "output": "hs" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "hs" }
            ],names
        )
    else:
        title = u"What are the shrinking product exports in {bra_id}?".format(**names)
        apps = app_obj(
            [
                { "app_name": "tree_map", "bra_id": bra_id, "output": "hs" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "hs" },
                { "app_name": "tree_map", "bra_id": bra_id, "output": "isic" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "isic" }
            ],names
        )
    
    recs = True
    
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)

@mod.route('/location/<bra_id>/opportunity/<ind_type>/')
def guide_location_opportunity(bra_id = None, ind_type = None):
    g.page_type = "plan"
    
    names = get_names({ "bra_id": bra_id })
    outfit = "travel"
    
    if ind_type == "industries":
        title = u"What are some local industry opportunites for {bra_id}?".format(**names)
        apps = app_obj(
            [
                { "app_name": "network", "bra_id": bra_id, "output": "isic" },
                { "app_name": "pie_scatter", "bra_id": bra_id, "output": "isic" },
                { "app_name": "tree_map", "bra_id": bra_id, "output": "isic" },
                { "app_name": "stacked", "bra_id": bra_id, "output": "cbo" },
                { "app_name": "tree_map", "bra_id": bra_id, "output": "cbo" }
            ],names
        )
    else:
        title = u"What are some product export opportunities for {bra_id}?".format(**names)
        apps = app_obj(
            [
                { "app_name": "network", "bra_id": bra_id, "output": "hs" },
                { "app_name": "pie_scatter", "bra_id": bra_id, "output": "hs" },
                { "app_name": "tree_map", "bra_id": bra_id, "output": "hs" },
                { "app_name": "tree_map", "bra_id": bra_id, "output": "wld" }
            ],names
        )

    recs = None
    
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)

@mod.route('/career/all/growth/<bra_id>/')
def guide_career_growth_all(bra_id = None):
    g.page_type = "plan"
    
    names = get_names({ "bra_id": bra_id })
    outfit = "preppy"
    
    title = u"What are the fastest growing jobs in {bra_id}?".format(**names)
    apps = app_obj(
        [
            { "app_name": "tree_map", "bra_id": bra_id, "output": "cbo" },
            { "app_name": "stacked", "bra_id": bra_id, "output": "cbo" }
        ],names
    )
    
    recs = True
    
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)

@mod.route('/career/all/wages/<bra_id>/')
def guide_career_wages(bra_id = None):
    g.page_type = "plan"
    
    names = get_names({ "bra_id": bra_id })
    outfit = "preppy"
    
    title = u"What are the best paid jobs in {bra_id}?".format(**names)
    apps = app_obj(
        [
            { "app_name": "tree_map", "bra_id": bra_id, "output": "cbo" },
            { "app_name": "stacked", "bra_id": bra_id, "output": "cbo" }
        ],names
    )
    
    recs = True
    
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)

@mod.route('/career/<cbo_id>/industries/<bra_id>/')
def guide_career_industries(bra_id = None, cbo_id = None):
    g.page_type = "plan"
    
    names = get_names({ "bra_id": bra_id, "cbo_id": cbo_id })
    outfit = "preppy"
    
    title = u"Which industries employ {cbo_id} in {bra_id}?".format(**names)
    apps = app_obj(
        [
            { "app_name": "tree_map", "bra_id": bra_id, "cbo_id": cbo_id, "output": "isic" },
            { "app_name": "tree_map", "bra_id": bra_id, "cbo_id": cbo_id, "output": "bra" },
            { "app_name": "stacked", "bra_id": bra_id, "cbo_id": cbo_id, "output": "bra" }
        ],names
    )
    
    recs = True
    
    if len(bra_id) == 8:
        recs = None
    else:
        recs = rec_list({ "bra_id": bra_id, "cbo_id": cbo_id },"bra",["wage"]);
    
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)

@mod.route('/career/<cbo_id>/paths/<bra_id>/')
def guide_career_paths(cbo_id = None, bra_id = None):
    g.page_type = "plan"
    
    names = get_names({ "cbo_id": cbo_id, "bra_id": bra_id })
    outfit = "preppy"
    
    title = u"Which are some common career paths for {cbo_id}?".format(**names)
    apps = app_obj(
        [
            { "app_name": "rings", "cbo_id": cbo_id, "output": "cbo" },
            { "app_name": "tree_map", "cbo_id": cbo_id, "output": "bra" },
            { "app_name": "tree_map", "cbo_id": cbo_id, "output": "isic" }
        ],names
    )
    
    recs = True
    
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)

@mod.route('/career/<cbo_id>/growth/<bra_id>/')
def guide_career_growth(bra_id = None, cbo_id = None):
    g.page_type = "plan"
    
    names = get_names({ "bra_id": bra_id, "cbo_id": cbo_id })
    outfit = "preppy"
    
    title = u"Where is employment of {cbo_id} growing?".format(**names)
    apps = app_obj(
        [
            { "app_name": "tree_map", "cbo_id": cbo_id, "output": "bra" },
            { "app_name": "tree_map", "cbo_id": cbo_id, "output": "isic" },
            { "app_name": "stacked", "cbo_id": cbo_id, "output": "bra" }
        ],names
    )
    
    recs = True
    
    return render_template("general/guide.html", outfit = outfit, title = title, 
        primary = apps[:1][0], secondaries = apps[1:], recs = recs)


###############################
# Get names from available ids
# ---------------------------
def get_names(params):
    
    obj = {}
    
    for name in params:
        if name == "ind_id":
            if len(params[name]) in [1,5]:
                model_name = "Isic"
            else:
                model_name = "Hs"
        else:
            model_name = name.split("_")[0].capitalize()
        model = getattr(attrs,model_name)
        if params[name] == "all":
            obj[name] = attrs.Wld.query.get_or_404("sabra").name_en
        else:
            obj[name] = model.query.get_or_404(params[name]).name_en
            
    return obj
        

###############################
# Guide page apps creator
# ---------------------------
def app_obj(apps,text):
    
    app_array = []    
    
    for params in apps:
        
        # If bra_id is null, set to "all"
        if params.get("bra_id") == None:
            params["bra_id"] = "all"
            text["bra_id"] = attrs.Wld.query.get_or_404("sabra").name_en
            
        # If output is null, set it to a default
        if params.get("output") == None:
            if params["app_name"] == "geo_map":
                params["output"] = "bra"
            elif params["app_name"] == "bubbles":
                params["output"] = "cbo"
            elif params["app_name"] == "rings":
                if "isic_id" in params:
                    params["output"] = "isic"
                elif "hs_id" in params:
                    params["output"] = "hs"
                else:
                    params["output"] = "cbo"
            else:
                params["output"] = "hs"
    
        # Set data_type based on what variables are available
        if "isic_id" in params or "cbo_id" in params or params["output"] in ["cbo","isic"]:
            params["data_type"] = "rais"
        else:
            params["data_type"] = "secex"
    
        obj = app_text(params,text)
        obj["url"] = app_url(params)
        print obj["url"]
        app_array.append(obj)
    
    return app_array


###############################
# Guide page app text generator
# ---------------------------
def app_text(params,text):
    
    texts = {
        "tree_map": {
            "short": u"<b>Tree Map</b> showing {category} share in {bra_id}.",
            "long": u"Here, we see that the top {list_number} {category_pl} are: {list}"
        },
        "stacked": {
            "short": u"<b>Stacked Area Chart</b> showing {category} share over time in {bra_id}.",
            "long": u"Here, we see that the top {list_number} {category_pl} are: {list}"
        },
        "network": {
            "short": u"<b>{category_title} Space</b> for {bra_id}.",
            "long": u"Here, we see that the top {list_number} {category_pl} are: {list}"
        },
        "rings": {
            "short": u"<b>Rings</b> showing {category} connections.",
            "long": u"Here, we see that the top {list_number} {category_pl} are: {list}"
        },
        "geo_map": {
            "short": u"<b>Geo Map</b> showing {category_pl} in {bra_id}.",
            "long": u"Here, we see that the top {list_number} {category_pl} are {list}"
        },
        "bubbles": {
            "short": u"<b>Occugrid</b> showing workforce needed for {ind_id}.",
            "long": u"Here, we see that the top {list_number} {category_pl} are: {list}"
        },
        "pie_scatter": {
            "short": u"<b>Scatter Plot</b> showing {category} distance and complexity for {bra_id}.",
            "long": u"Here, we see that the top {list_number} {category_pl} are: {list}"
        }
    }
    
    text["list_number"] = 5

    if params["output"] is "isic":
        text["category"] = "industry"
        text["category_pl"] = "industries"
        text["category_title"] = "Industry"
        length = 5
    elif params["output"] is "cbo":
        text["category"] = "occupation"
        text["category_pl"] = "occupations"
        text["category_title"] = "Occupation"
        length = 4
    elif params["output"] is "hs":
        text["category"] = "product"
        text["category_pl"] = "products"
        text["category_title"] = "Product"
        length = 6
    elif params["output"] is "wld":
        text["category"] = "trade partner"
        text["category_pl"] = "trade partners"
        length = 5
    elif params["output"] is "bra":
        text["category"] = "municipality"
        text["category_pl"] = "municipalities"
        length = 8
    
    def get_list():

        model_name = "Y"
        filters = {}
        if params["bra_id"] != "all" or params["output"] == "bra":
            model_name += "b"
        if params["data_type"] is "rais":
            if "isic_id" in params or params["output"] is "isic":
                model_name += "i"
                if "isic_id" in params:
                    filters["isic_id"] = params["isic_id"]
            if "cbo_id" in params or params["output"] is "cbo":
                model_name += "o"
                if "cbo_id" in params:
                    filters["cbo_id"] = params["cbo_id"]
            model = getattr(rais,model_name)
            sort = "wage"
        elif params["data_type"] is "secex":
            if "hs_id" in params or params["output"] is "hs":
                model_name += "p"
                if "hs_id" in params:
                    filters["hs_id"] = params["hs_id"]
            if "wld_id" in params or params["output"] is "wld":
                model_name += "w"
                if "wld_id" in params:
                    filters["wld_id"] = params["wld_id"]
            model = getattr(secex,model_name)
            sort = "val_usd"
        
        list_array = model.query \
            .filter_by(**filters) \
            .filter(model.year == func.max(model.year).select()) \
            .filter(func.char_length(getattr(model,"{0}_id".format(params["output"]))) == length)
            
        if params["bra_id"] != "all":
            if params["app_name"] is "geo_map":
                list_array = list_array \
                    .filter(model.bra_id.startswith(params["bra_id"]))
            else:
                list_array = list_array \
                    .filter(model.bra_id == params["bra_id"])
                
        list_array = list_array \
            .order_by(model.year.desc(),getattr(model,sort).desc()) \
            .limit(text["list_number"])
        
        names = []
        for l in list_array.all():
            type = params["output"]
            if type == "hs":
                cat = "product"
            elif type == "isic":
                cat = "industry"
            elif type == "cbo":
                cat = "occupation"
            elif type == "bra":
                cat = "location"
            elif type == "wld":
                cat = "partner"
                
            names.append(u"<a href='/browse/{0}/{1}') }}'>{2}</a>".format(cat,getattr(l,type).id,getattr(l,type).name_en))

        
        list_txt = ", ".join(names)
        
        return list_txt
        
    text["list"] = get_list()
    
    obj = {
        "text_short": texts[params["app_name"]]["short"].format(**text),
        "text_long": texts[params["app_name"]]["long"].format(**text)
    }
    
    return obj
    


###############################
# URL generator for embedded apps
# ---------------------------
# Requires app_name, the rest are optional
def app_url(params):
    
    # Set data_type and filters based on what variables are available
    if params["data_type"] is "rais":
        fs = ["isic_id","cbo_id"]
    elif params["data_type"] is "secex":
        fs = ["hs_id","wld_id"]
        
    # Fill null filters with "all"
    for i, f in enumerate(fs):
        if f in params:
            fs[i] = params[f]
        else:
            fs[i] = "all"

    # Get embedded url based off of variables
    url = url_for("apps.embed", app_name = params["app_name"], \
        data_type = params["data_type"], bra_id = params["bra_id"], filter1 = fs[0], \
        filter2 = fs[1], output = params["output"], builder = "false")
    
    return url
    

    
def rec_list(filters,output,lists):

    model_name = "Y"
    
    if "ind_id" in filters:
        if len(filters["ind_id"]) in [1,5]:
            filters["isic_id"] = filters["ind_id"]
        else:
            filters["hs_id"] = filters["ind_id"]
        del filters["ind_id"]
    
    if output == "bra" or "bra_id" in filters:
        model_name += "b"

    if "isic_id" in filters or "cbo_id" in filters:
        if "isic_id" in filters:
            model_name += "i"
        if "cbo_id" in filters:
            model_name += "o"
        model = getattr(rais,model_name)
    if "hs_id" in filters or "wld_id" in filters:
        if "hs_id" in filters:
            model_name += "p"
        if "wld_id" in filters:
            model_name += "w"
        model = getattr(secex,model_name)
    
    bra_id = filters["bra_id"]
    del filters["bra_id"]
    
    rec_obj = {}
    for sort in lists:
        
        if sort in ["rca_min","rca_max"]:
            value = "rca"
        else:
            value = sort
        
        list_array = model.query \
            .filter_by(**filters) \
            .filter(model.year == func.max(model.year).select())
        
        if output == "bra":
        
            if bra_id == "all" or bra_id == None:
                list_array = list_array \
                    .filter(func.char_length(getattr(model,"bra_id")) == 2)
            else:
                list_array = list_array \
                    .filter(model.bra_id.startswith(bra_id)) \
                    .filter(func.char_length(getattr(model,"bra_id")) == 8)
        
        list_array = list_array \
            .filter(getattr(model,value) != None)
            
        if sort == "rca_min":
            list_array = list_array \
                .filter(getattr(model,value) > 0) \
                .order_by(getattr(model,value).asc())
        elif sort == "rca_max":
            list_array = list_array \
                .filter(getattr(model,value) >= 1) \
                .order_by(getattr(model,value).desc())
        else:
            list_array = list_array \
                .order_by(getattr(model,value).desc())
                

        list_array = list_array \
            .limit(20)
    
        rec_array = []
        for l in list_array:
            name = getattr(l,output).name_en
            id = getattr(l,output).id
            color = getattr(l,output).color
            val = getattr(l,value)
            url = request.environ['PATH_INFO'].replace(bra_id,id)
            rec_array.append({"name": name, "id": id, "color": color, "value": val, "url": url})
        rec_obj[sort] = rec_array
    
    return {"type": output, "lists": rec_obj}


###############################
# Guide selection breadcrumb view
# ---------------------------
@mod.route('/')
@mod.route('/<category>/')
@mod.route('/<category>/<category_id>/')
@mod.route('/<category>/<category_id>/<option>/')
def guide(category = None, category_id = None, option = None):
    
    item = None
    article = None
    
    if option:
        page = "guide/location.html"
    elif category_id:
        if category_id == "select":
            page = "general/selector.html".format(category)
        else:
            if category_id != "all":
                if category == "establishment":
                    item = attrs.Isic.query.get_or_404(category_id)
                elif category == "export":
                    item = attrs.Hs.query.get_or_404(category_id)
                elif category == "career":
                    item = attrs.Cbo.query.get_or_404(category_id)
                elif category == "location":
                    item = attrs.Bra.query.get_or_404(category_id)
            elif category == "location":
                item = attrs.Wld.query.get_or_404("sabra")
            page = "guide/{0}.html".format(category)
    elif category == "industry":
        page = "guide/industry.html"
    elif category:
        page = "guide/choice.html"
    else:
        page = "guide/index.html"
        
    if category == "career":
        article = "an occupation"
    elif category == "establishment":
        article = "an industry"
    elif category == "export":
        article = "a product"
    elif category == "location":
        article = "a location"
        
    if category != None:
        g.sabrina["face"] = "smirk"
    
    if category == "career":
        g.sabrina["outfit"] = "preppy"
    elif category == "industry" or category == "export" or category == "establishment":
        g.sabrina["outfit"] = "worker"
        if category == "export" or category == "establishment":
            g.sabrina["hat"] = "hardhat"
    elif category == "location":
        g.sabrina["outfit"] = "travel"
        
    if category_id == "select":
        g.sabrina["outfit"] = g.sabrina["outfit"]+"_presenting"
            
    return render_template(page,
        category = category,
        category_id = category_id,
        option = option,
        item = item,
        article = article)
