import MySQLdb, time, sys, os, math
import pandas as pd, pandas.io.sql as sql
import numpy as np

from os import environ

this_dir = os.path.abspath(os.path.dirname(__file__))
base_dir = os.path.abspath(os.path.join(this_dir, '../../../'))

growth_lib_dir = os.path.abspath(os.path.join(base_dir, 'scripts/growth_lib/'))
sys.path.append(growth_lib_dir)
import growth

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()


def get_ybio_panel(**kwargs):
    q = """
        select 
          ybio.bra_id, isic_id, cbo_id, num_emp / num_est as avg_num_emp
        from 
          rais_ybio as ybio
        where 
          ybio.year = {0} and 
          length(ybio.bra_id) = {1} and 
          length(ybio.isic_id) = 5 and
          length(ybio.cbo_id) = 4
        """.format(kwargs["year"], kwargs["geo_level"])
    table = sql.read_frame(q, db)
    table = table.pivot_table(rows=["isic_id", "cbo_id"], cols="bra_id", values="avg_num_emp")
    table = table.fillna(0)

    panel = table.to_panel()
    
    return panel

def get_mcp(**kwargs):
    year = kwargs["year"]
    '''mcp'''
    q = """
        select 
          yg.bra_id, isic_id, {0} 
        from 
          rais_ybi as ygi, attrs_yb as yg
        where 
          yg.year = {1} and 
          yg.year = ygi.year and 
          length(yg.bra_id) = {2} and 
          length(ygi.isic_id) = {3} and 
          yg.population > {4} and 
          ygi.bra_id = yg.bra_id
      """.format(kwargs["val"], kwargs["year"], kwargs["geo_level"], 5, kwargs["pop_cutoff"])
    # print q
    mcp = sql.read_frame(q, db)
    mcp = mcp.pivot(index="bra_id", columns="isic_id", values=kwargs["val"])
    mcp = mcp.fillna(0)
    
    return mcp

def main(**kwargs):
    year = kwargs["year"]
    mcp_wage = get_mcp(year=kwargs["year"], geo_level=kwargs["geo_level"], 
                    pop_cutoff=kwargs["pop_cutoff"], val="wage")
    mcp_num_emp = get_mcp(year=kwargs["year"], geo_level=kwargs["geo_level"], 
                    pop_cutoff=kwargs["pop_cutoff"], val="num_emp")
    print "loading YBIO table..." 
    ybio_panel = get_ybio_panel(year=kwargs["year"], 
                    geo_level=kwargs["geo_level"])
    
    rcas = growth.rca(mcp_wage)
    rcas[rcas >= 1] = 1
    rcas[rcas < 1] = 0
    
    prox = growth.proximity(rcas.T)
    
    s = time.time()
    for geo in rcas.index:
        print year, geo, time.time() - s
        s = time.time()
        
        # reset array of items to add
        to_add = []
        
        # this_state_emps = pd.DataFrame([mcp_num_emp.ix[geo].values]*len(mcp_num_emp.index), index=mcp_num_emp.index, columns=mcp_num_emp.columns)
        avg_ranks = prox[geo].rank(ascending=False).dropna()
        
        for isic in rcas.columns:
            
            # filter ranking for only those that HAVE RCA by multiplying by 0
            best_isic_matches = rcas[isic] * avg_ranks
            best_isic_matches = best_isic_matches[best_isic_matches > 0]
            
            if not len(best_isic_matches):
                continue
            
            # if this location has RCA just use its required
            if best_isic_matches.order().index[0] == geo:
                required_geos = [geo]
            
            # elif len(best_isic_matches) == 1:
            #     required_geo = best_isic_matches.order().index[0]
            
            # take top 20%
            num_geos = math.ceil(len(best_isic_matches) *.2)
            required_geos = list(best_isic_matches.order()[:num_geos].index)
            
            required_cbos = None
            for g in required_geos:
                if required_cbos is None:
                    required_cbos = pd.DataFrame(ybio_panel[g].ix[isic].fillna(0), columns=[g])
                else:
                    required_cbos[g] = ybio_panel[g].ix[isic].fillna(0)
                # required_cbos = ybio_panel[g].ix[isic].fillna(0)
                # required_cbos = required_cbos[required_cbos > 0]
            
            required_cbos = required_cbos.mean(axis=1)
            required_cbos = required_cbos[required_cbos >= 1]
            
            # print required_cbos
            # sys.exit()
            
            for cbo in required_cbos.index:
                to_add.append([year, geo, isic, cbo, required_cbos[cbo], required_cbos[cbo]])
            
            # print to_add
            # sys.exit()
            
        # add to db
        cursor.executemany("INSERT INTO rais_ybio (year, bra_id, isic_id, "\
            "cbo_id, required) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY "\
            "UPDATE required=%s;", to_add)

if __name__ == "__main__":
    pop_cutoff = 0
    # pop_cutoff = 150000
    # val_cutoff = 1000000000
    val_cutoff = 0
    for year in range(2010, 2012):
        print year
        for geo_level in [2, 4, 7, 8]:
            print geo_level
            main(year=year, geo_level=geo_level, pop_cutoff=pop_cutoff, val_cutoff=val_cutoff)