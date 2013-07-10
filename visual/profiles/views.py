from flask import Blueprint, request, render_template, g, url_for
from sqlalchemy import func

from visual import db
from visual.attrs import models as attrs
from visual.rais import models as rais
from visual.secex import models as secex

mod = Blueprint('profiles', __name__, url_prefix='/profiles')

@mod.before_request
def before_request():
    g.page_type = mod.name
    
    g.sabrina = {}
    g.sabrina["outfit"] = "lab"
    g.sabrina["face"] = "smirk"
    g.sabrina["hat"] = None
    
    g.path = request.path

@mod.route('/')
def profiles():
    return render_template("profiles/index.html")

@mod.route('/career/<cbo_id>/')
def profiles_cbo(cbo_id = None):
    
    if cbo_id == "select":

        article = "an occupation"
        
        return render_template("general/selector.html", 
            category = "career",
            article = article)
        
    else:
        g.page_type = "profile"
    
        names = get_names({ "cbo_id": cbo_id })
    
        title = u"{cbo_id}".format(**names)
        outfit = "preppy"
    
        apps = app_obj(
            [
                { "app_name": "rings", "cbo_id": cbo_id },
                { "app_name": "tree_map", "cbo_id": cbo_id, "output": "bra" },
                { "app_name": "tree_map", "cbo_id": cbo_id, "output": "isic" }
            ],names
        )
    
        rec = False
    
        return render_template("general/guide.html", outfit = outfit, title = title, 
            primary = apps[:1][0], secondaries = apps[1:], rec = rec)

@mod.route('/establishment/<isic_id>/')
def profiles_isic(isic_id = None):
    
    if isic_id == "select":

        article = "an industry"
        
        return render_template("general/selector.html", 
            category = "establishment",
            article = article)
        
    else:
        g.page_type = "profile"
    
        names = get_names({ "isic_id": isic_id })
    
        title = u"{isic_id}".format(**names)
        outfit = "worker"
    
        apps = app_obj(
            [
                { "app_name": "rings", "isic_id": isic_id },
                { "app_name": "tree_map", "isic_id": isic_id, "output": "bra" },
                { "app_name": "bubbles", "isic_id": isic_id },
                { "app_name": "tree_map", "isic_id": isic_id, "output": "cbo" }
            ],names
        )
    
        rec = False
    
        return render_template("general/guide.html", outfit = outfit, title = title, 
            primary = apps[:1][0], secondaries = apps[1:], rec = rec)

@mod.route('/export/<hs_id>/')
def profiles_hs(hs_id = None):
    
    if hs_id == "select":

        article = "a product"
        
        return render_template("general/selector.html", 
            category = "export",
            article = article)
        
    else:
        g.page_type = "profile"
    
        names = get_names({ "hs_id": hs_id })
    
        title = u"{hs_id}".format(**names)
        outfit = "worker"
    
        apps = app_obj(
            [
                { "app_name": "rings", "hs_id": hs_id },
                { "app_name": "tree_map", "hs_id": hs_id, "output": "bra" },
                { "app_name": "tree_map", "hs_id": hs_id, "output": "wld" }
            ],names
        )
    
        rec = False
    
        return render_template("general/guide.html", outfit = outfit, title = title, 
            primary = apps[:1][0], secondaries = apps[1:], rec = rec)

@mod.route('/location/<bra_id>/')
def profiles_bra(bra_id = None):
    
    if bra_id == "select":

        article = "a location"
        
        return render_template("general/selector.html", 
            category = "location",
            article = article)
        
    else:
        g.page_type = "profile"
    
        names = get_names({ "bra_id": bra_id })
    
        title = u"{bra_id}".format(**names)
        outfit = "travel"
    
        apps = app_obj(
            [
                { "app_name": "network", "bra_id": bra_id, "output": "hs" },
                { "app_name": "network", "bra_id": bra_id, "output": "isic" },
                { "app_name": "tree_map", "bra_id": bra_id, "output": "cbo" },
                { "app_name": "pie_scatter", "bra_id": bra_id, "output": "hs" },
                { "app_name": "tree_map", "bra_id": bra_id, "output": "isic" }
            ],names
        )
    
        rec = False
    
        return render_template("general/guide.html", outfit = outfit, title = title, 
            primary = apps[:1][0], secondaries = apps[1:], rec = rec)

@mod.route('/partner/<wld_id>/')
def profiles_wld(wld_id = None):
    
    if wld_id == "select":

        article = "a trade partner"
        
        return render_template("general/selector.html", 
            category = "partner",
            article = article)
        
    else:
        g.page_type = "profile"
    
        names = get_names({ "wld_id": wld_id })
    
        title = u"{wld_id}".format(**names)
        outfit = "travel"
    
        apps = app_obj(
            [
                { "app_name": "tree_map", "wld_id": wld_id, "output": "hs" },
                { "app_name": "tree_map", "wld_id": wld_id, "output": "bra" },
                { "app_name": "stacked", "wld_id": wld_id, "output": "hs" }
            ],names
        )
    
        rec = False
    
        return render_template("general/guide.html", outfit = outfit, title = title, 
            primary = apps[:1][0], secondaries = apps[1:], rec = rec)
    
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
            names.append(u"<a href='/profiles/{0}/{1}') }}'>{2}</a>".format(cat,getattr(l,type).id,getattr(l,type).name_en))
        
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