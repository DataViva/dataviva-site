from dataviva.stats.util import parse_year
from sqlalchemy import desc
from dataviva import __year_range__

from dataviva.attrs.models import  University, Course_hedu, Course_sc, Stat, Bs
from dataviva.attrs.models import Yb, Ybs, Bra, Hs, Cbo, Cnae, Wld
from dataviva.secex.models import Ymbp, Ymbw, Ympw, Ymb, Ymp, Ymw
from dataviva.rais.models import Ybi, Ybo, Yio, Yb_rais, Yi, Yo
from dataviva.hedu.models import Yu, Yuc, Ybu, Yc_hedu
from dataviva.sc.models import Ybc_sc, Yc_sc

from flask.ext.babel import gettext


def bra_stats(pobj, rais_year, secex_year):
    stats = []
    group = "General Stats"
    stat_ids = ["pop", "gini", "life_exp", "hdi", "gdp", "gdp_pc", "pop_density"]
    stats_year = parse_year(__year_range__["stats"][-1].split("-")[0])
    results = batch_stats(Ybs, pobj.id, stat_ids, stats_year)
    for name, val in results.items():
        stats.append(make_stat(group, name, desc=val, year=stats_year))

    group = '{} Stats ({}):'.format(rais_year, "RAIS")
    filters = [Ybi.year == rais_year, Ybi.bra_id == pobj.id, Ybi.cnae_id_len == 6]
    result = get_top_stat(Ybi, Ybi.cnae_id, Ybi.num_emp, Cnae, filters)
    if result:
        profile, value = result
        stat = make_stat(group, gettext("Top Industry by Employment"), profile=profile, value=value, mode="num_emp")
        stats.append(stat)

    filters = [Ybo.year == rais_year, Ybo.bra_id == pobj.id, Ybo.cbo_id_len == 4]
    profile, value = get_top_stat(Ybo, Ybo.cbo_id, Ybo.num_emp, Cbo, filters)
    stat = make_stat(group, gettext("Top Occupation by Employment"), profile=profile, value=value, mode="num_emp")
    stats.append(stat)

    value = get_stat_val(Yb_rais, Yb_rais.wage, [Yb_rais.year == rais_year, Yb_rais.bra_id == pobj.id])
    stats.append(make_stat(group, gettext("Total Monthly Wage"), desc=value, mode="wage"))

    group = '{} Stats ({}):'.format(secex_year, "SECEX")
    filters = [Ymbp.year == secex_year, Ymbp.month == 0, Ymbp.bra_id == pobj.id, Ymbp.hs_id_len == 6]
    result = get_top_stat(Ymbp, Ymbp.hs_id, Ymbp.export_val, Hs, filters)
    if result:
        profile, value = result
        stat = make_stat(group, gettext("Top Product by Export Value"), profile=profile, value=value, mode="export_val")
        stats.append(stat)

    filters = [Ymbw.year == secex_year, Ymbw.month == 0, Ymbw.bra_id == pobj.id, Ymbw.wld_id_len == 5]
    result = get_top_stat(Ymbw, Ymbw.wld_id, Ymbw.export_val, Wld, filters)
    if result:
        profile,value=result
        stats.append(make_stat(group, gettext("Top Destination by Export Value"), profile=profile, value=value, mode="export_val"))

    filters = [Ymb.year == secex_year, Ymb.month == 0, Ymb.bra_id == pobj.id]
    result = get_stat_val(Ymb, [Ymb.export_val, Ymb.import_val], filters)
    if result:
        export_val, import_val = result
        stats.append(make_stat(group, gettext("Total Exports"), desc=export_val, mode="export_val"))
        stats.append(make_stat(group, gettext("Total Imports"), desc=import_val, mode="export_val"))
    
    if len(pobj.id) > 1:
        geo = Bra.query.get(pobj.id[:1])
        stats.append(make_stat("General Stats", gettext("Region"), profile=geo))
    if len(pobj.id) > 3:
        geo = Bra.query.get(pobj.id[:3])
        stats.append(make_stat("General Stats", gettext("State"), profile=geo))
    if len(pobj.id) > 5:
        geo = Bra.query.get(pobj.id[:5])
        stats.append(make_stat("General Stats", gettext("Mesoregion"), profile=geo))
    if len(pobj.id) > 7:
        geo = Bra.query.get(pobj.id[:7])
        stats.append(make_stat("General Stats", gettext("Microregion"), profile=geo))
    
    if len(pobj.id) == 9:
        group = "General Stats"
        stat_ids = ["airport", "airport_dist", "seaport", "seaport_dist", "area", "capital_dist", "neighbors"]
        results = batch_stats(Bs, pobj.id, stat_ids)
        for name, val in results.items():
            if name.lower() == "neighbors":
                bras = Bra.query.filter(Bra.id.in_(val.split(","))).all()
                val = ", ".join([u"<a href='{}'>{}</a>".format(b.url(), b.name()) for b in bras])
            stats.append(make_stat(group, name, desc=val))
    return stats

def cnae_stats(pobj, rais_year):
    stats = []
    five_years_ago = rais_year - 5
    group = '{} Stats ({}):'.format(rais_year, "RAIS")

    filters = [Ybi.year == rais_year, Ybi.cnae_id == pobj.id, Ybi.bra_id_len == 9]
    profile, value = get_top_stat(Ybi, Ybi.bra_id, Ybi.num_emp, Bra, filters)
    stats.append(make_stat(group, gettext("Top Municipality by Employment"), profile=profile, value=value, mode="num_emp"))

    filters = [Yio.year == rais_year, Yio.cnae_id == pobj.id, Yio.cbo_id_len == 4]
    profile, value = get_top_stat(Yio, Yio.cbo_id, Yio.num_emp, Cbo, filters)
    stats.append(make_stat(group, gettext("Top Occupation by Employment"), profile=profile, value=value, mode="num_emp"))

    filters = [Yi.year == rais_year, Yi.cnae_id == pobj.id]
    wage, wage_avg = get_stat_val(Yi, [Yi.wage, Yi.wage_avg], filters)
    stats.append(make_stat(group, gettext("Total Monthly Wage"), desc=wage, mode="wage"))
    stats.append(make_stat(group, gettext("Average Monthly Wage"), desc=wage_avg, mode="wage"))

    group = '{} Stats ({}):'.format(five_years_ago, "RAIS")
    wage, wage_avg = get_stat_val(Yi, [Yi.wage, Yi.wage_avg], filters)
    filters = [Yi.year == five_years_ago, Yi.cnae_id == pobj.id]
    wage, wage_avg = get_stat_val(Yi, [Yi.wage, Yi.wage_avg], filters)
    stats.append(make_stat(group, gettext("Total Monthly Wage"), desc=wage, mode="wage"))
    stats.append(make_stat(group, gettext("Average Monthly Wage"), desc=wage_avg, mode="wage"))
    return stats

def cbo_stats(pobj, rais_year):
    stats = []
    five_years_ago = rais_year - 5
    group = '{} Stats ({}):'.format(rais_year, "RAIS")

    filters = [Ybo.year == rais_year, Ybo.cbo_id == pobj.id, Ybo.bra_id_len == 9]
    profile, value = get_top_stat(Ybo, Ybo.bra_id, Ybo.num_emp, Bra, filters)
    stats.append(make_stat(group, gettext("Top Municipality by Employment"), profile=profile, value=value, mode="num_emp"))

    filters = [Yio.year == rais_year, Yio.cbo_id == pobj.id, Yio.cnae_id_len == 6]
    profile, value = get_top_stat(Yio, Yio.cnae_id, Yio.num_emp, Cnae, filters)
    stats.append(make_stat(group, gettext("Top Industry by Employment"), profile=profile, value=value, mode="num_emp"))

    filters = [Yo.year == rais_year, Yo.cbo_id == pobj.id]
    res = get_stat_val(Yo, [Yo.wage, Yo.wage_avg], filters)
    if res:
        wage, wage_avg = res
        stats.append(make_stat(group, gettext("Total Monthly Wage"), desc=wage, mode="wage"))
        stats.append(make_stat(group, gettext("Average Monthly Wage"), desc=wage_avg, mode="wage"))

    group = '{} Stats ({}):'.format(five_years_ago, "RAIS")
    filters = [Yo.year == five_years_ago, Yo.cbo_id == pobj.id]
    res = get_stat_val(Yo, [Yo.wage, Yo.wage_avg], filters)
    if res:
        wage, wage_avg = res
        stats.append(make_stat(group, gettext("Total Monthly Wage"), desc=wage, mode="wage"))
        stats.append(make_stat(group, gettext("Average Monthly Wage"), desc=wage_avg, mode="wage"))
    return stats


def hs_stats(pobj, secex_year):
    stats =[]
    group = '{} Stats ({}):'.format(secex_year, "SECEX")
    five_years_ago = secex_year - 5

    filters = [Ymbp.year == secex_year, Ymbp.month == 0, Ymbp.hs_id == pobj.id, Ymbp.bra_id_len == 9]
    profile, value = get_top_stat(Ymbp, Ymbp.bra_id, Ymbp.export_val, Bra, filters)
    stats.append(make_stat(group, gettext("Top Municipality by Exports"), profile=profile, value=value, mode="export_val"))

    filters = [Ympw.year == secex_year, Ympw.month == 0, Ympw.hs_id == pobj.id, Ympw.wld_id_len == 5]
    profile, value = get_top_stat(Ympw, Ympw.wld_id, Ympw.export_val, Wld, filters)
    stats.append(make_stat(group, gettext("Top Country by Exports"), profile=profile, value=value, mode="export_val"))

    filters = [Ymp.year == secex_year, Ymp.month == 0, Ymp.hs_id == pobj.id]
    g1, g5, total_exports = get_stat_val(Ymp, [Ymp.export_val_growth, Ymp.export_val_growth_5, Ymp.export_val], filters)
    stats.append(make_stat(group, gettext("Nominal Annual Growth Rate (1 year)"), desc=g1, mode="export_val_growth"))
    stats.append(make_stat(group, gettext("Nominal Annual Growth Rate (5 year)"), desc=g5, mode="export_val_growth"))
    stats.append(make_stat(group, gettext("Total Exports"), desc=total_exports, mode="export_val"))

    group = '{} Stats ({}):'.format(five_years_ago, "SECEX")
    filters = [Ymp.year == five_years_ago, Ymp.month == 0, Ymp.hs_id == pobj.id]
    total_exports = get_stat_val(Ymp, Ymp.export_val, filters)
    stats.append(make_stat(group, gettext("Total Exports"), desc=total_exports, mode="export_val"))
    return stats

def wld_stats(pobj, secex_year):
    stats = []
    dataset = "secex"
    five_years_ago = secex_year - 5

    group = '{} Stats ({}):'.format(secex_year, "SECEX")
    filters = [Ymbw.year == secex_year, Ymbw.month == 0, Ymbw.wld_id == pobj.id, Ymbw.bra_id_len == 9]
    profile, value = get_top_stat(Ymbw, Ymbw.bra_id, Ymbw.export_val, Bra, filters)
    stats.append(make_stat(group, gettext("Top Destination by Export Value"), profile=profile, value=value, mode="export_val"))

    filters = [Ympw.year == secex_year, Ympw.month == 0, Ympw.wld_id == pobj.id, Ympw.hs_id_len == 6]
    profile, value = get_top_stat(Ympw, Ympw.hs_id, Ympw.export_val, Hs, filters)
    stat = make_stat(group, gettext("Top Product by Export Value"), profile=profile, value=value, mode="export_val")
    stats.append(stat)

    filters = [Ymw.year == secex_year, Ymw.month == 0, Ymw.wld_id == pobj.id]
    g1e, g5e, total_exports, g1i, g5i, total_imports, eci = get_stat_val(Ymw, [Ymw.export_val_growth, Ymw.export_val_growth_5, Ymw.export_val, Ymw.import_val_growth, Ymw.import_val_growth_5, Ymw.import_val, Ymw.eci], filters)
    stats.append(make_stat(group, gettext("Total Imports"), desc=total_exports, mode="import_val"))
    stats.append(make_stat(group, gettext("Nominal Annual Growth Rate (1 year)"), desc=g1i, mode="import_val_growth"))
    stats.append(make_stat(group, gettext("Nominal Annual Growth Rate (5 year)"), desc=g5i, mode="import_val_growth"))
    stats.append(make_stat(group, gettext("Total Exports"), desc=total_exports, mode="export_val"))
    stats.append(make_stat(group, gettext("Nominal Annual Growth Rate (1 year)"), desc=g1e, mode="export_val_growth"))
    stats.append(make_stat(group, gettext("Nominal Annual Growth Rate (5 year)"), desc=g5e, mode="export_val_growth"))
    stats.append(make_stat(group, gettext("Economic Complexity"), desc=eci, mode="eci"))

    group = '{} Stats ({}):'.format(five_years_ago, "SECEX")
    filters = [Ymw.year == five_years_ago, Ymw.month == 0, Ymw.wld_id == pobj.id]

    total_exports, total_imports, eci = get_stat_val(Ymw, [Ymw.export_val, Ymw.import_val, Ymw.eci], filters)
    stats.append(make_stat(group, gettext("Total Exports"), desc=total_exports, mode="export_val"))
    stats.append(make_stat(group, gettext("Total Imports"), desc=total_imports, mode="import_val"))
    stats.append(make_stat(group, gettext("Economic Complexity"), desc=eci, mode="eci"))
    return stats


def university_stats(pobj, hedu_year):
    stats = []
    group = '{} Stats ({}):'.format(hedu_year, "HEDU")
    filters = [Yuc.year == hedu_year, Yuc.university_id == pobj.id, Yuc.course_hedu_id_len == 6]
    profile, value = get_top_stat(Yuc, Yuc.course_hedu_id, Yuc.enrolled, Course_hedu, filters)
    stats.append(make_stat(group, gettext("Top Course by Enrollment"), profile=profile, value=value, mode="enrolled"))

    filters = [Yu.year == hedu_year, Yu.university_id == pobj.id]
    enrolled, graduates = get_stat_val(Ymw, [Yu.enrolled, Yu.graduates], filters)
    stats.append(make_stat(group, gettext("Total Enrollment"), desc=enrolled, mode="enrolled"))
    stats.append(make_stat(group, gettext("Total Graduates"), desc=graduates, mode="graduates"))
    return stats

def course_hedu_stats(pobj, hedu_year):
    stats = []
    group = '{} Stats ({}):'.format(hedu_year, "HEDU")

    filters = [Yuc.year == hedu_year, Yuc.course_hedu_id == pobj.id] # -- no nesting for university_ids
    profile, value = get_top_stat(Yuc, Yuc.university_id, Yuc.enrolled, University, filters)
    stats.append(make_stat(group, gettext("Top University by Enrollment"), profile=profile, value=value, mode="enrolled"))

    filters = [Yc_hedu.year == hedu_year, Yc_hedu.course_hedu_id == pobj.id]
    enrolled, graduates = get_stat_val(Ymw, [Yc_hedu.enrolled, Yc_hedu.graduates], filters)
    stats.append(make_stat(group, gettext("Total Enrollment"), desc=enrolled, mode="enrolled"))
    stats.append(make_stat(group, gettext("Total Graduates"), desc=graduates, mode="graduates"))
    return stats

def course_sc_stats(pobj):
    stats = []
    sc_year = parse_year(__year_range__["sc"][-1].split("-")[0])
    group = '{} Stats ({}):'.format(sc_year, "SC")

    filters = [Ybc_sc.year == sc_year, Ybc_sc.course_sc_id == pobj.id, Ybc_sc.bra_id_len == 9]
    profile, value = get_top_stat(Ybc_sc, Ybc_sc.bra_id, Ybc_sc.enrolled, Bra, filters)
    stats.append(make_stat(group, gettext("Top Municipality by Enrollment"), profile=profile, value=value, mode="enrolled"))

    filters = [Yc_sc.year == sc_year, Yc_sc.course_sc_id == pobj.id]
    enrolled, age = get_stat_val(Ymw, [Yc_sc.enrolled, Yc_sc.age], filters)
    stats.append(make_stat(group, gettext("Total Enrollment"), desc=enrolled, mode="enrolled"))
    stats.append(make_stat(group, gettext("Average Age"), desc=age, mode="graduates"))
    return stats

def compute_stats(pobj):
    attr_type = pobj.__class__.__name__.lower()
    stats = []
    if attr_type == "wld" and pobj.id == "all":
        attr_type = "bra"

    rais_year = parse_year(__year_range__["rais"][-1].split("-")[0])
    secex_year = parse_year(__year_range__["secex"][-1].split("-")[0])
    hedu_year = parse_year(__year_range__["hedu"][-1].split("-")[0])

    if attr_type == "bra":
        return bra_stats(pobj, rais_year, secex_year)
    elif attr_type == "cnae":
        return cnae_stats(pobj, rais_year)
    elif attr_type == "cbo":
        return cbo_stats(pobj, rais_year)
    elif attr_type == "hs":
        return hs_stats(pobj, secex_year)
    elif attr_type == "wld":
        return wld_stats(pobj, secex_year)
    elif attr_type == "university":
        return university_stats(pobj, hedu_year)
    elif attr_type == "course_hedu":
        return course_hedu_stats(pobj, hedu_year)
    elif attr_type == "course_sc":
        return course_sc_stats(pobj)

    return stats


def batch_stats(Tbl, bra_id, stat_ids, year=None):
    filters = [Tbl.stat_id.in_(stat_ids), Tbl.bra_id == bra_id]
    if year:
        filters.append(Tbl.year == year)
    results = Tbl.query.join(Stat).with_entities(Stat, Tbl.stat_val).filter(*filters).all()

    values = {stat.name() : val for stat,val in results}
    return values

def get_stat_val(Tbl, metric_col, filters):
    if not type(metric_col) == list:
        q = Tbl.query.with_entities(metric_col).filter(*filters)
        res, = q.first()
        return res
    else:
        q = Tbl.query.with_entities(*metric_col).filter(*filters)
        return q.first()

def get_top_stat(Tbl, show_col, metric_col, Profile, filters):
    q = Tbl.query.with_entities(show_col, metric_col).filter(*filters)
    res = q.order_by(desc(metric_col)).first()
    if res:
        pk, val = res
        profile = Profile.query.get(pk)
        return profile, val
    return res

def make_stat(group, name, desc=None, value=None, url=None, mode=None, year=None, profile=None):
    if year:
        name += " ({})".format(year)

    if profile:
        url = profile.url()
        desc = profile.name()

    if not value:
        if not desc:
            desc = gettext("-")

    return {
                'group': group,
                'name': name,
                'url': url,
                'desc' : desc,
                'value': value,
                'mode' : mode,
    }
