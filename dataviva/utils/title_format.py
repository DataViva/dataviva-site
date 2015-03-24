import re
from flask import g
from flask.ext.babel import gettext

from .title_case import title_case

def title_format(title, attr):

    if not isinstance(attr, (list, tuple)):
        attr = [attr]

    joiner = " {} ".format(gettext("and"))
    type = attr[0].__class__.__name__.lower()

    names = []
    for a in attr:
        name = title_case(getattr(a, "name_{}".format(g.locale)))
        if hasattr(a, "distance") and a.id != "all" and a.distance > 0:
            name = name + " "+a.distance+"km"
        names.append(name)

    article_search = re.search("<{}_(\w+)>".format(type), title)
    if article_search:
        title = title.replace(" <{}>".format(type), "")
        title = title.replace(article_search.group(0), joiner.join([get_article(attr[i], article_search.group(1)) + " " + names[i] for i, b in enumerate(names)]))
    else:
        title = title.replace("<{}>".format(type), joiner.join(names))

    return title

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
