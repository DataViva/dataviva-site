# -*- coding: utf-8 -*-
import math
from flask import g
from flask.ext.babel import gettext, pgettext
from babel.numbers import format_decimal
from dataviva.translations.dictionary import plurals

def affixes(key=None, unit=False):

    affixes = {
        "airport_dist": "km",
        "area": "km2",
        "capital_dist": "km",
        "elevation": "km",
        "enrolled": "stu",
        "entrants": "stu",
        "export_val": "usd",
        "graduates": "stu",
        "import_val": "usd",
        "gdp": "brl",
        "gdp_pc": "brl",
        "num_jobs": "jobs",
        "purchase_value": "brl",
        "seaport_dist": "km",
        "students": "stu",
        "transfer_value": "brl",
        "wage": "brl",
        "wage_avg": "brl",
        "wage_avg_bra": "brl"
    }

    if unit:
        if key:
            return affixes[key] if key in affixes else None
        return affixes

    affixTypes = {
        "brl": ["BRL ", ""],
        "km": ["", "km"],
        "km2": ["", u"km²"],
        "jobs": ["", u" {0}".format(gettext("jobs"))],
        "stu": ["", u" {0}".format(gettext("students"))],
        "usd": ["USD ", ""]
    }

    if key:
        return affixTypes[affixes[key]] if key in affixes else None

    returnDict = {}
    for a, v in affixes.iteritems():
        returnDict[a] = affixTypes[v]
    return returnDict

def num_format(number, key = None, labels = True):

    if key == "ordinal":

        ordinals = (pgettext('0', 'th'),
                    pgettext('1', 'st'),
                    pgettext('2', 'nd'),
                    pgettext('3', 'rd'),
                    pgettext('4', 'th'),
                    pgettext('5', 'th'),
                    pgettext('6', 'th'),
                    pgettext('7', 'th'),
                    pgettext('8', 'th'),
                    pgettext('9', 'th'))

        n = int(number)
        if n % 100 in (11, 12, 13):
            return "{0}{1}".format(n, ordinals[0])
        return "{0}{1}".format(n, ordinals[n % 10])

    # Converts the number to a float.
    try:
        n = float(number)
    except ValueError:
        return number
    label  = None
    suffix = None

    # Determines which index of "groups" to move the decimal point to.
    if n:

        groups = ["", "k", "M", "B", "T"]
        m = max(0,min(len(groups)-1, int(math.floor(math.log10(abs(n))/3))))

        # Moves the decimal point and rounds the new number to specific decimals.
        n = n/10**(3*m)
        if n > 99:
            n = int(n)
        elif n > 9:
            n = round(n, 1)
        elif n > 1:
            n = round(n, 2)
        else:
            n = round(n, 3)

        # Initializes the number suffix based on the group.
        suffix = groups[m]

    arrow = False
    if "growth" in key:
        if n > 0:
            arrow = "up"
        elif n < 0:
            arrow = "down"
        n = float(n)*100
    n = format_decimal(n, locale=g.locale)

    # If the language is not English, translate the suffix.
    if suffix:
        if g.locale != "en":
            suffix = u" {0}".format(plurals(key=suffix, n=n))
        n = u"{0}{1}".format(n,suffix)

    if key and labels:
        affix = affixes(key)
        if affix:
            return u"{0}{1}{2}".format(unicode(affix[0]), n, unicode(affix[1]))
        elif "growth" in key:
            if arrow:
                arrow = "<i class='growth-arrow {0} fa fa-arrow-circle-{0}'></i>".format(arrow)
            else:
                arrow = ""
            return "{}%{}".format(n, arrow)

    return n
