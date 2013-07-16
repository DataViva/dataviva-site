from flask import Blueprint, request, render_template, g, url_for
from sqlalchemy import func
from datetime import datetime

from visual import db
from visual.attrs import models as attrs
from visual.rais import models as rais
from visual.secex import models as secex

from visual.general.models import Plan

mod = Blueprint('guide', __name__, url_prefix='/guide')

@mod.before_request
def before_request():
    
    g.page_type = mod.name
    
    g.sabrina = {}
    g.sabrina["outfit"] = "casual"
    g.sabrina["face"] = "smile"
    g.sabrina["hat"] = None
    
    g.path = request.path


# ###############################
# # Guide page apps creator
# # ---------------------------

# def rec_list(filters,output,lists):
# 
#     model_name = "Y"
#     
#     if "ind_id" in filters:
#         if len(filters["ind_id"]) in [1,5]:
#             filters["isic_id"] = filters["ind_id"]
#         else:
#             filters["hs_id"] = filters["ind_id"]
#         del filters["ind_id"]
#     
#     if output == "bra" or "bra_id" in filters:
#         model_name += "b"
# 
#     if "isic_id" in filters or "cbo_id" in filters:
#         if "isic_id" in filters:
#             model_name += "i"
#         if "cbo_id" in filters:
#             model_name += "o"
#         model = getattr(rais,model_name)
#     if "hs_id" in filters or "wld_id" in filters:
#         if "hs_id" in filters:
#             model_name += "p"
#         if "wld_id" in filters:
#             model_name += "w"
#         model = getattr(secex,model_name)
#     
#     bra_id = filters["bra_id"]
#     del filters["bra_id"]
#     
#     rec_obj = {}
#     for sort in lists:
#         
#         if sort in ["rca_min","rca_max"]:
#             value = "rca"
#         else:
#             value = sort
#         
#         list_array = model.query \
#             .filter_by(**filters) \
#             .filter(model.year == func.max(model.year).select())
#         
#         if output == "bra":
#         
#             if bra_id == "all" or bra_id == None:
#                 list_array = list_array \
#                     .filter(func.char_length(getattr(model,"bra_id")) == 2)
#             else:
#                 list_array = list_array \
#                     .filter(model.bra_id.startswith(bra_id)) \
#                     .filter(func.char_length(getattr(model,"bra_id")) == 8)
#         
#         list_array = list_array \
#             .filter(getattr(model,value) != None)
#             
#         if sort == "rca_min":
#             list_array = list_array \
#                 .filter(getattr(model,value) > 0) \
#                 .order_by(getattr(model,value).asc())
#         elif sort == "rca_max":
#             list_array = list_array \
#                 .filter(getattr(model,value) >= 1) \
#                 .order_by(getattr(model,value).desc())
#         else:
#             list_array = list_array \
#                 .order_by(getattr(model,value).desc())
#                 
# 
#         list_array = list_array \
#             .limit(20)
#     
#         rec_array = []
#         for l in list_array:
#             name = getattr(l,output).name_en
#             id = getattr(l,output).id
#             color = getattr(l,output).color
#             val = getattr(l,value)
#             url = request.environ['PATH_INFO'].replace(bra_id,id)
#             rec_array.append({"name": name, "id": id, "color": color, "value": val, "url": url})
#         rec_obj[sort] = rec_array
#     
#     return {"type": output, "lists": rec_obj}


###############################
# Guide selection breadcrumb view
# ---------------------------

@mod.route('/')
@mod.route('/<category>/')
@mod.route('/<category>/<category_id>/')
@mod.route('/<category>/<category_id>/<option>/')
@mod.route('/<category>/<category_id>/<option>/<option_id>/')
@mod.route('/<category>/<category_id>/<option>/<option_id>/<extra_id>/')
def guide(category = None, category_id = None, option = None, subject = None, option_id = None, extra_id = None):
    
    item = None
    article = None
    title = None
    selector = category
    recs = False
    plan = None
    
    bra_id = "all"
    filter1 = None
    filter2 = None
    
    category_type = category_id
    option_type = option_id
    extra_type = extra_id
        
    if category == "career":
        if category_id != "all":
            category_type = "<cbo>"
        if option_id and option_id != "select":
            option_type = "<bra>"
    elif category == "export":
        category_type = "<hs>"
        if option == "potential" and option_id and option_id != "select":
            option_type = "<bra>"
    elif category == "establishment":
        category_type = "<isic>"
        if option == "potential":
            option_type = "<bra>"
    elif category == "location":
        category_type = "<bra>"
        if option == "establishment" and option_id:
            option_type = "<isic>"
        if option_id == "export" and extra_id and extra_id != "select":
            extra_type = "<hs>"
        elif option_id == "establishment" and extra_id and extra_id != "select":
            extra_type = "<isic>"
    elif category == "partner":
        category_type = "<wld>"
    # raise Exception(category,category_type,option,option_type,extra_type)
    plan = Plan.query.filter_by(category=category, category_type=category_type, option=option, option_type=option_type, option_id=extra_type).first()
    # raise Exception(plan)
    if plan:
        
        g.page_type = "plan"
        page = "general/guide.html"
        
        if category == "career":
            plan.set_attr(category_id,"cbo")
            filter2 = category_id
        elif category == "export":
            plan.set_attr(category_id,"hs")
            filter1 = category_id
        elif category == "establishment":
            plan.set_attr(category_id,"isic")
            filter1 = category_id
        elif category == "partner":
            plan.set_attr(category_id,"wld")
            filter2 = category_id

        if category == "location":
            plan.set_attr(category_id,"bra")
            if option_id == "export" and extra_id:
                plan.set_attr(extra_id,"hs")
                filter1 = extra_id
            elif option_id == "establishment" and extra_id:
                plan.set_attr(extra_id,"isic")
                filter1 = extra_id
            bra_id = category_id    
        elif option_type == "<bra>":
            plan.set_attr(option_id,"bra")
            bra_id = option_id
            
        builds = [0]*len(plan.builds.all())
        for pb in plan.builds.all():
            build = {}
            pb.build.all()[0].set_bra(bra_id)
            if filter1:
                pb.build.all()[0].set_filter1(filter1)
            if filter2:
                pb.build.all()[0].set_filter2(filter2)
                
            build["url"] = "/apps/embed/{0}{1}".format(pb.build.all()[0].url(),pb.variables)
            builds[pb.position-1] = build
            
        plan = {"title": plan.title(), "builds": builds}
            
    elif extra_id == "select":
        page = "general/selector.html"
        selector = option_id
    elif option_id == "select":
        page = "general/selector.html"
        selector = "location"
    elif option:
        if category == "career":
            selector = "location"
            page = "guide/choice.html"
        elif category == "location":
            page = "guide/industry.html"
        elif category == "export" and option == "potential":
            selector = "location"
            page = "guide/choice.html"
    elif category_id:
        if category_id == "select":
            page = "general/selector.html"
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
        
    if selector == "career":
        article = "an occupation"
    elif selector == "establishment":
        article = "an industry"
    elif selector == "export":
        article = "a product"
    elif selector == "location":
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
        
    # if len(option_id) == 8:
    #     recs = None
    # else:
    #     recs = rec_list({ "bra_id": option_id, "cbo_id": option_id },"bra",["wage"]);
            
    return render_template(page,
        category = category,
        category_id = category_id,
        option = option,
        item = item,
        article = article,
        title = title,
        selector = selector,
        plan = plan)
