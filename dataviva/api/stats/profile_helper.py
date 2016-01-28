from dataviva.api.stats.util import parse_year
from sqlalchemy import desc
from dataviva import __year_range__

from dataviva.api.attrs.models import  University, Course_hedu, Course_sc, Stat, Bs
from dataviva.api.attrs.models import Yb, Ybs, Bra, Hs, Cbo, Cnae, Wld
from dataviva.api.secex.models import Ymbp, Ymbw, Ympw, Ymb, Ymp, Ymw
from dataviva.api.rais.models import Ybi, Ybo, Yio, Yb_rais, Yi, Yo
from dataviva.api.hedu.models import Yu, Yuc, Ybu, Yc_hedu
from dataviva.api.sc.models import Ybc_sc, Yc_sc

from dataviva.utils.title_case import title_case

from flask.ext.babel import gettext


def bra_stats(pobj, rais_year, secex_year):
    stats = []

    gen_title = gettext("General Stats")
    key = "general"

    if pobj.id != "all":
        stat_ids = ["pop", "gini", "life_exp", "hdi", "gdp", "gdp_pc", "pop_density"]
        stats_year = parse_year(__year_range__["stats"][-1].split("-")[0])
        results = batch_stats(Ybs, pobj.id, stat_ids, stats_year)
        for stat, val in results:
            stats.append(make_stat(key, gen_title, stat.name(), desc=val, year=stats_year, mode=stat.id))

    group = u'{1} {0}'.format(gettext("Employment Stats"), rais_year)
    key = "rais"
    if pobj.id == "all":
        filters = [Yi.year == rais_year, Yi.cnae_id_len == 6]
        result = get_top_stat(Yi, Yi.cnae_id, Yi.num_jobs, Cnae, filters)
    else:
        filters = [Ybi.year == rais_year, Ybi.bra_id == pobj.id, Ybi.cnae_id_len == 6]
        result = get_top_stat(Ybi, Ybi.cnae_id, Ybi.num_jobs, Cnae, filters)
    if result:
        profile, value = result
        stat = make_stat(key, group, gettext("Top Industry by Employment"), profile=profile, value=value, mode="num_jobs")
        stats.append(stat)

    if pobj.id == "all":
        filters = [Yo.year == rais_year, Yo.cbo_id_len == 4]
        profile, value = get_top_stat(Yo, Yo.cbo_id, Yo.num_jobs, Cbo, filters)
    else:
        filters = [Ybo.year == rais_year, Ybo.bra_id == pobj.id, Ybo.cbo_id_len == 4]
        profile, value = get_top_stat(Ybo, Ybo.cbo_id, Ybo.num_jobs, Cbo, filters)
    stat = make_stat(key, group, gettext("Top Occupation by Employment"), profile=profile, value=value, mode="num_jobs")
    stats.append(stat)

    if pobj.id != "all":
        value = get_stat_val(Yb_rais, Yb_rais.wage, [Yb_rais.year == rais_year, Yb_rais.bra_id == pobj.id])
        stats.append(make_stat(key, group, gettext("Total Monthly Wage"), desc=value, mode="wage"))

    group = u'{1} {0}'.format(gettext("Trade Stats"), secex_year)
    key = "secex"
    if pobj.id == "all":
        filters = [Ymp.year == secex_year, Ymp.month == 0, Ymp.hs_id_len == 6]
        result = get_top_stat(Ymp, Ymp.hs_id, Ymp.export_val, Hs, filters)
    else:
        filters = [Ymbp.year == secex_year, Ymbp.month == 0, Ymbp.bra_id == pobj.id, Ymbp.hs_id_len == 6]
        result = get_top_stat(Ymbp, Ymbp.hs_id, Ymbp.export_val, Hs, filters)
    if result:
        profile, value = result
        stat = make_stat(key, group, gettext("Top Product by Export Value"), profile=profile, value=value, mode="export_val")
        stats.append(stat)

    if pobj.id == "all":
        filters = [Ymw.year == secex_year, Ymw.month == 0, Ymw.wld_id_len == 5]
        result = get_top_stat(Ymw, Ymw.wld_id, Ymw.export_val, Wld, filters)
    else:
        filters = [Ymbw.year == secex_year, Ymbw.month == 0, Ymbw.bra_id == pobj.id, Ymbw.wld_id_len == 5]
        result = get_top_stat(Ymbw, Ymbw.wld_id, Ymbw.export_val, Wld, filters)
    if result:
        profile,value=result
        stats.append(make_stat(key, group, gettext("Top Destination by Export Value"), profile=profile, value=value, mode="export_val"))

    if pobj.id != "all":
        filters = [Ymb.year == secex_year, Ymb.month == 0, Ymb.bra_id == pobj.id]
        result = get_stat_val(Ymb, [Ymb.export_val, Ymb.import_val], filters)
        if result:
            export_val, import_val = result
            stats.append(make_stat(key, group, gettext("Total Exports"), desc=export_val, mode="export_val"))
            stats.append(make_stat(key, group, gettext("Total Imports"), desc=import_val, mode="export_val"))

        key = "general"
        if len(pobj.id) > 1:
            geo = Bra.query.get(pobj.id[:1])
            stats.append(make_stat(key, gen_title, gettext("Region"), profile=geo))
        if len(pobj.id) > 3:
            geo = Bra.query.get(pobj.id[:3])
            stats.append(make_stat(key, gen_title, gettext("State"), profile=geo))
        if len(pobj.id) > 5:
            geo = Bra.query.get(pobj.id[:5])
            stats.append(make_stat(key, gen_title, gettext("Mesoregion"), profile=geo))
        if len(pobj.id) > 7:
            geo = Bra.query.get(pobj.id[:7])
            stats.append(make_stat(key, gen_title, gettext("Microregion"), profile=geo))

        if len(pobj.id) == 9:
            stat_ids = ["airport", "airport_dist", "seaport", "seaport_dist", "area", "capital_dist", "neighbors"]
            results = batch_stats(Bs, pobj.id, stat_ids)
            for stat, val in results:
                if stat.id == "neighbors":
                    bras = Bra.query.filter(Bra.id.in_(val.split(","))).all()
                    val = ", ".join([u"<a href='{}'>{}</a>".format(b.url(), b.name()) for b in bras])
                stats.append(make_stat(key, gen_title, stat.name(), desc=val, mode=stat.id))

    return stats

def cnae_stats(pobj, rais_year):
    stats = []
    five_years_ago = rais_year - 5
    group = u'{1} {0}'.format(gettext("Employment Stats"), rais_year)
    key = "rais"

    filters = [Ybi.year == rais_year, Ybi.cnae_id == pobj.id, Ybi.bra_id_len == 9]
    profile, value = get_top_stat(Ybi, Ybi.bra_id, Ybi.num_jobs, Bra, filters)
    stats.append(make_stat(key, group, gettext("Top Municipality by Employment"), profile=profile, value=value, mode="num_jobs"))

    filters = [Yio.year == rais_year, Yio.cnae_id == pobj.id, Yio.cbo_id_len == 4]
    profile, value = get_top_stat(Yio, Yio.cbo_id, Yio.num_jobs, Cbo, filters)
    stats.append(make_stat(key, group, gettext("Top Occupation by Employment"), profile=profile, value=value, mode="num_jobs"))

    filters = [Yi.year == rais_year, Yi.cnae_id == pobj.id]
    wage, wage_avg, num_est, age_avg = get_stat_val(Yi, [Yi.wage, Yi.wage_avg, Yi.num_est, Yi.age_avg], filters)
    stats.append(make_stat(key, group, gettext("Total Monthly Wage"), desc=wage, mode="wage"))
    stats.append(make_stat(key, group, gettext("Average Monthly Wage"), desc=wage_avg, mode="wage"))
    stats.append(make_stat(key, group, gettext("Total Establishments"), desc=num_est, mode="num_est"))
    stats.append(make_stat(key, group, gettext("Average Employee Age"), desc=age_avg, mode="age"))

    group = u'{1} {0}'.format(gettext("Employment Stats"), five_years_ago)
    wage, wage_avg = get_stat_val(Yi, [Yi.wage, Yi.wage_avg], filters)
    filters = [Yi.year == five_years_ago, Yi.cnae_id == pobj.id]
    wage, wage_avg = get_stat_val(Yi, [Yi.wage, Yi.wage_avg], filters)
    stats.append(make_stat(key, group, gettext("Total Monthly Wage"), desc=wage, mode="wage"))
    stats.append(make_stat(key, group, gettext("Average Monthly Wage"), desc=wage_avg, mode="wage"))
    return stats

def cbo_stats(pobj, rais_year):
    stats = []
    five_years_ago = rais_year - 5
    group = u'{1} {0}'.format(gettext("Employment Stats"), rais_year)
    key = "rais"

    filters = [Ybo.year == rais_year, Ybo.cbo_id == pobj.id, Ybo.bra_id_len == 9]
    profile, value = get_top_stat(Ybo, Ybo.bra_id, Ybo.num_jobs, Bra, filters)
    stats.append(make_stat(key, group, gettext("Top Municipality by Employment"), profile=profile, value=value, mode="num_jobs"))

    filters = [Yio.year == rais_year, Yio.cbo_id == pobj.id, Yio.cnae_id_len == 6]
    profile, value = get_top_stat(Yio, Yio.cnae_id, Yio.num_jobs, Cnae, filters)
    stats.append(make_stat(key, group, gettext("Top Industry by Employment"), profile=profile, value=value, mode="num_jobs"))

    filters = [Yo.year == rais_year, Yo.cbo_id == pobj.id]
    res = get_stat_val(Yo, [Yo.wage, Yo.wage_avg, Yo.age_avg], filters)
    if res:
        wage, wage_avg, age_avg = res
        stats.append(make_stat(key, group, gettext("Total Monthly Wage"), desc=wage, mode="wage"))
        stats.append(make_stat(key, group, gettext("Average Monthly Wage"), desc=wage_avg, mode="wage"))
        stats.append(make_stat(key, group, gettext("Average Employee Age"), desc=age_avg, mode="age"))

    group = u'{1} {0}'.format(gettext("Employment Stats"), five_years_ago)
    filters = [Yo.year == five_years_ago, Yo.cbo_id == pobj.id]
    res = get_stat_val(Yo, [Yo.wage, Yo.wage_avg], filters)
    if res:
        wage, wage_avg = res
        stats.append(make_stat(key, group, gettext("Total Monthly Wage"), desc=wage, mode="wage"))
        stats.append(make_stat(key, group, gettext("Average Monthly Wage"), desc=wage_avg, mode="wage"))
    return stats


def hs_stats(pobj, secex_year):
    stats =[]
    group = u'{1} {0}'.format(gettext("Trade Stats"), secex_year)
    key = "secex"
    five_years_ago = secex_year - 5

    filters = [Ymbp.year == secex_year, Ymbp.month == 0, Ymbp.hs_id == pobj.id, Ymbp.bra_id_len == 9]
    top_stat = get_top_stat(Ymbp, Ymbp.bra_id, Ymbp.export_val, Bra, filters)
    if top_stat:
        stats.append(make_stat(key, group, gettext("Top Municipality by Exports"), profile=top_stat[0], value=top_stat[1], mode="export_val"))

    filters = [Ympw.year == secex_year, Ympw.month == 0, Ympw.hs_id == pobj.id, Ympw.wld_id_len == 5]
    top_stat = get_top_stat(Ympw, Ympw.wld_id, Ympw.export_val, Wld, filters)
    if top_stat:
        stats.append(make_stat(key, group, gettext("Top Country by Exports"), profile=top_stat[0], value=top_stat[1], mode="export_val"))

    filters = [Ymp.year == secex_year, Ymp.month == 0, Ymp.hs_id == pobj.id]
    stat_val = get_stat_val(Ymp, [Ymp.export_val_growth, Ymp.export_val_growth_5, Ymp.export_val, Ymp.import_val], filters)
    if stat_val:
        g1, g5, total_exports, total_imports = stat_val
        stats.append(make_stat(key, group, gettext("Nominal Annual Growth Rate (1 year)"), desc=g1, mode="export_val_growth"))
        stats.append(make_stat(key, group, gettext("Nominal Annual Growth Rate (5 year)"), desc=g5, mode="export_val_growth"))
        stats.append(make_stat(key, group, gettext("Total Exports"), desc=total_exports, mode="export_val"))
        stats.append(make_stat(key, group, gettext("Total Imports"), desc=total_imports, mode="import_val"))

    group = u'{1} {0}'.format(gettext("Trade Stats"), five_years_ago)
    filters = [Ymp.year == five_years_ago, Ymp.month == 0, Ymp.hs_id == pobj.id]
    total_exports = get_stat_val(Ymp, Ymp.export_val, filters)
    stats.append(make_stat(key, group, gettext("Total Exports"), desc=total_exports, mode="export_val"))
    return stats

def wld_stats(pobj, secex_year):
    stats = []
    dataset = "secex"
    five_years_ago = secex_year - 5

    group = u'{1} {0}'.format(gettext("Trade Stats"), secex_year)
    key = "secex"
    filters = [Ymbw.year == secex_year, Ymbw.month == 0, Ymbw.wld_id == pobj.id, Ymbw.bra_id_len == 9]
    profile, value = get_top_stat(Ymbw, Ymbw.bra_id, Ymbw.export_val, Bra, filters)
    stats.append(make_stat(key, group, gettext("Top Destination by Export Value"), profile=profile, value=value, mode="export_val"))

    filters = [Ympw.year == secex_year, Ympw.month == 0, Ympw.wld_id == pobj.id, Ympw.hs_id_len == 6]
    profile, value = get_top_stat(Ympw, Ympw.hs_id, Ympw.export_val, Hs, filters)
    stat = make_stat(key, group, gettext("Top Product by Export Value"), profile=profile, value=value, mode="export_val")
    stats.append(stat)

    filters = [Ymw.year == secex_year, Ymw.month == 0, Ymw.wld_id == pobj.id]
    g1e, g5e, total_exports, g1i, g5i, total_imports, eci = get_stat_val(Ymw, [Ymw.export_val_growth, Ymw.export_val_growth_5, Ymw.export_val, Ymw.import_val_growth, Ymw.import_val_growth_5, Ymw.import_val, Ymw.eci], filters)
    stats.append(make_stat(key, group, gettext("Total Imports"), desc=total_imports, mode="import_val"))
    stats.append(make_stat(key, group, gettext("Nominal Annual Growth Rate (1 year)"), desc=g1i, mode="import_val_growth"))
    stats.append(make_stat(key, group, gettext("Nominal Annual Growth Rate (5 year)"), desc=g5i, mode="import_val_growth"))
    stats.append(make_stat(key, group, gettext("Total Exports"), desc=total_exports, mode="export_val"))
    stats.append(make_stat(key, group, gettext("Nominal Annual Growth Rate (1 year)"), desc=g1e, mode="export_val_growth"))
    stats.append(make_stat(key, group, gettext("Nominal Annual Growth Rate (5 year)"), desc=g5e, mode="export_val_growth"))
    stats.append(make_stat(key, group, gettext("Economic Complexity"), desc=eci, mode="eci"))

    group = u'{1} {0}'.format(gettext("Trade Stats"), five_years_ago)
    filters = [Ymw.year == five_years_ago, Ymw.month == 0, Ymw.wld_id == pobj.id]

    total_exports, total_imports, eci = get_stat_val(Ymw, [Ymw.export_val, Ymw.import_val, Ymw.eci], filters)
    stats.append(make_stat(key, group, gettext("Total Exports"), desc=total_exports, mode="export_val"))
    stats.append(make_stat(key, group, gettext("Total Imports"), desc=total_imports, mode="import_val"))
    stats.append(make_stat(key, group, gettext("Economic Complexity"), desc=eci, mode="eci"))
    return stats


def university_stats(pobj, hedu_year):
    stats = []

    gen_title = gettext("General Stats")
    key = "general"
    filters = [Ybu.year == hedu_year, Ybu.university_id == pobj.id, Ybu.bra_id_len == 9, Ybu.bra_id != "0xx000007"]
    campuses, num_campuses = get_top_stats(Ybu, Ybu.bra_id, Ybu.enrolled, Bra, filters, max=5)
    if num_campuses:
        val = ", ".join([u"<a href='{}'>{}</a>".format(c[0].url(), c[0].name()) for c in campuses])
        if num_campuses > len(campuses):
            val += "<br /> +{} more".format(num_campuses-len(campuses))
        if num_campuses > 1:
            stats.append(make_stat(key, gen_title, gettext("Top Campuses"), desc=val))
        else:
            stats.append(make_stat(key, gen_title, gettext("Location"), desc=val))
    stats.append(make_stat(key, gen_title, gettext("Administrative Dependency"), desc=pobj.school_type()))

    group = u'{1} {0}'.format(gettext("Enrollment Stats"), hedu_year)
    key = "hedu"
    filters = [Yuc.year == hedu_year, Yuc.university_id == pobj.id, Yuc.course_hedu_id_len == 6]
    profile, value = get_top_stat(Yuc, Yuc.course_hedu_id, Yuc.enrolled, Course_hedu, filters)
    stats.append(make_stat(key, group, gettext("Top Major by Enrollment"), profile=profile, value=value, mode="enrolled"))

    filters = [Yu.year == hedu_year, Yu.university_id == pobj.id]
    stat_vals = get_stat_val(Ymw, [Yu.enrolled, Yu.graduates], filters)
    if stat_vals:
        enrolled, graduates = stat_vals
        # raise Exception(enrolled, graduates)
        stats.append(make_stat(key, group, gettext("Total Enrollment"), desc=enrolled, mode="enrolled"))
        stats.append(make_stat(key, group, gettext("Total Graduates"), desc=graduates, mode="graduates"))
    return stats

def course_hedu_stats(pobj, hedu_year):
    stats = []
    group = u'{1} {0}'.format(gettext("Enrollment Stats"), hedu_year)
    key = "hedu"

    filters = [Yuc.year == hedu_year, Yuc.course_hedu_id == pobj.id] # -- no nesting for university_ids
    top_stat = get_top_stat(Yuc, Yuc.university_id, Yuc.enrolled, University, filters)
    if top_stat:
        stats.append(make_stat(key, group, gettext("Top University by Enrollment"), profile=top_stat[0], value=top_stat[1], mode="enrolled"))

    filters = [Yc_hedu.year == hedu_year, Yc_hedu.course_hedu_id == pobj.id]
    stat_val = get_stat_val(Ymw, [Yc_hedu.enrolled, Yc_hedu.graduates], filters)
    if stat_val:
        enrolled, graduates = stat_val
        stats.append(make_stat(key, group, gettext("Total Enrollment"), desc=enrolled, mode="enrolled"))
        stats.append(make_stat(key, group, gettext("Total Graduates"), desc=graduates, mode="graduates"))
    return stats

def course_sc_stats(pobj):
    stats = []
    sc_year = parse_year(__year_range__["sc"][-1].split("-")[0])
    group = u'{1} {0}'.format(gettext("Enrollment Stats"), sc_year)
    key = "hedu"

    filters = [Ybc_sc.year == sc_year, Ybc_sc.course_sc_id == pobj.id, Ybc_sc.bra_id_len == 9]
    profile, value = get_top_stat(Ybc_sc, Ybc_sc.bra_id, Ybc_sc.enrolled, Bra, filters)
    stats.append(make_stat(key, group, gettext("Top Municipality by Enrollment"), profile=profile, value=value, mode="enrolled"))

    filters = [Yc_sc.year == sc_year, Yc_sc.course_sc_id == pobj.id]
    enrolled, age = get_stat_val(Ymw, [Yc_sc.enrolled, Yc_sc.age], filters)
    stats.append(make_stat(key, group, gettext("Total Enrollment"), desc=enrolled, mode="enrolled"))
    stats.append(make_stat(key, group, gettext("Average Age"), desc=age, mode="graduates"))
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
    return results
    #
    # values = {stat.name() : val for stat,val in results}
    # return values

def get_stat_val(Tbl, metric_col, filters):
    if not type(metric_col) == list:
        q = Tbl.query.with_entities(metric_col).filter(*filters)
        res = q.first()
        if res:
            return res[0]
        else:
            return None
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
    return (None, None)

def get_top_stats(Tbl, show_col, metric_col, Profile, filters, max=5):
    q = Tbl.query.with_entities(show_col, metric_col).filter(*filters)
    res = q.order_by(desc(metric_col)).all()
    if res:
        top_stats = []
        for r in res[:max]:
            pk, val = r
            profile = Profile.query.get(pk)
            top_stats.append((profile, val))
        return top_stats, len(res)
    return ([], 0)

def make_stat(key, group, name, desc=None, value=None, url=None, mode=None, year=None, profile=None):
    if year:
        name += " ({})".format(year)

    if profile:
        url = profile.url()
        desc = profile.name()

    if not value:
        if not desc:
            desc = "-"

    return {
                "group": group,
                "key": key,
                "name": title_case(name),
                "url": url,
                "desc" : desc,
                "value": value,
                "mode" : mode
            }
