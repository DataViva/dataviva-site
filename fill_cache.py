# -*- coding: utf-8 -*-
'''
    Script to fill cache with most popular URLs
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    0. BEFORE RUNNING SCRIPT:
        - need to comment out redis sessions
        - need to comment out access session var
    1. Get unique attrs.
        Bras:
         - all
         - every state
         - top 10% of other municipalities by population
        ISIC & CBO:
         - every sector
         - top 10% by number of employees (5 digit, 4 digit)
        HS & WLD:
         - every sector/continent
         - top 10% by val_usd (6 digit, 5 digit)
    2. Create different URLs
    3. Ask server for URLs and let it cache them

History is written by the winners because in writing the history,
    you justify yourself.
~ George Orwell
'''

import MySQLdb, sys, itertools, urllib2, time, os
from os import environ

this_dir = os.path.abspath(os.path.dirname(__file__))
base_dir = os.path.abspath(os.path.join(this_dir, '../../../'))

visual_dir = os.path.abspath(os.path.join(base_dir, 'scripts/growth_lib/'))
sys.path.append(visual_dir)
from dataviva import app
from flask import g

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_uniques(table):
    uniques = []
    
    if table == "attrs_bra":
        
        '''Minas Gerais at the top of the state list'''
        uniques += ["mg"]
        
        '''Planning Regions in Minas Gerais'''
        q = "select id from attrs_bra where length(id) = 7;"
        cursor.execute(q)
        uniques += [row[0] for row in cursor.fetchall()]
        
        '''Municipalities in Minas Gerais'''
        q = "select bra_id from rais_yb where length(bra_id) = 8 and num_emp > 20000 and year = 2010 and substr(bra_id,1,2) = 'mg' order by num_emp desc;"
        cursor.execute(q)
        uniques += [row[0] for row in cursor.fetchall()]
        
        '''Other States'''
        q = "select bra_id from rais_yb where length(bra_id) = 2 and bra_id != 'mg' and year = 2010 order by num_emp desc;"
        cursor.execute(q)
        uniques += [row[0] for row in cursor.fetchall()]
        
        '''all of brazil'''
        uniques += ["all"]
        
        '''municipalities not in Minas Gerais'''
        q = "select bra_id from rais_yb where length(bra_id) = 8 and num_emp > 100000 and year = 2010 and substr(bra_id,1,2) != 'mg' order by num_emp desc;"
        cursor.execute(q)
        uniques += [row[0] for row in cursor.fetchall()]
        
        print "{0} Locations".format(len(uniques))
        
    elif table == "attrs_hs":
        
        '''HS2'''
        q = "select distinct(hs_id) from secex_yp where length(hs_id) = 2"
        cursor.execute(q)
        uniques += [row[0] for row in cursor.fetchall()]
        
        q = "select hs_id from secex_yp where length(hs_id) = 6 and val_usd > 500000000 and year = 2010;"
        cursor.execute(q)
        uniques += [row[0] for row in cursor.fetchall()]
        
        print "{0} Products".format(len(uniques))
        
    elif table == "attrs_cbo":
        
        '''CBO 1'''
        q = "select distinct(cbo_id) from rais_yo where length(cbo_id) = 1"
        cursor.execute(q)
        uniques += [row[0] for row in cursor.fetchall()]
        
        q = "select cbo_id from rais_yo where length(cbo_id) = 4 and num_emp > 200000 and year = 2010;"
        cursor.execute(q)
        uniques += [row[0] for row in cursor.fetchall()]
        
        print "{0} Products".format(len(uniques))
        
    elif table == "attrs_isic":
        
        '''ISIC top level'''
        q = "select distinct(isic_id) from rais_yi where length(isic_id) = 1"
        cursor.execute(q)
        uniques += [row[0] for row in cursor.fetchall()]
        
        q = "select isic_id from rais_yi where length(isic_id) = 5 and num_emp > 200000 and year = 2010;"
        cursor.execute(q)
        uniques += [row[0] for row in cursor.fetchall()]
        
        print "{0} Industries".format(len(uniques))
        
    elif table == "attrs_wld":
        
        '''continents'''
        q = "select distinct(wld_id) from secex_yw where length(wld_id) = 2"
        cursor.execute(q)
        uniques += [row[0] for row in cursor.fetchall()]
        
        q = "select wld_id from secex_yw where length(wld_id) = 5 and val_usd > 500000000 and year = 2010;"
        cursor.execute(q)
        uniques += [row[0] for row in cursor.fetchall()]
        
        print "{0} Countries".format(len(uniques))

    return uniques

def get_urls():
    
    urls = {"rais":[], "secex":[]}
    
    '''rais'''
    urls["rais"] = ['/rais/2010/{bra}/all/show.4/', '/rais/2010/{bra}/show.5/all/', \
            '/rais/2010/{bra}/{isic}/show.4/', '/rais/2010/{bra}/show.5/{cbo}/',
            '/rais/2010/{bra}.show.8/all/all/', '/rais/2010/{bra}.show.8/{isic}/all/', \
            '/rais/2010/{bra}.show.8/all/{cbo}/']
            
    # q = "select max(year) from rais_yb"
    # cursor.execute(q)
    # maxyear = cursor.fetchall()[0][0]
    # 
    # temp = []
    # for url in urls["rais"]:
    #     temp.append(url.replace("all",str(maxyear),1))
    #     
    # urls["rais"] = temp + urls["rais"]
    
    '''secex'''
    urls["secex"] = ['/secex/2011/{bra}/all/show.5/', '/secex/2011/{bra}/show.6/all/', \
            '/secex/2011/{bra}/{hs}/show.5/', '/secex/2011/{bra}/show.6/{wld}/',
            '/secex/2011/{bra}.show.8/all/all/', '/secex/2011/{bra}.show.8/{hs}/all/', \
            '/secex/2011/{bra}.show.8/all/{wld}/']
    
    # q = "select max(year) from secex_yb"
    # cursor.execute(q)
    # maxyear = cursor.fetchall()[0][0]
    # 
    # temp = []
    # for url in urls["secex"]:
    #     temp.append(url.replace("all",str(maxyear),1))
    #     
    # urls["secex"] = temp + urls["secex"]
    
    return urls

def format_urls(urls, attrs):
    
    print "Formatting URLs..."
    
    formatted_urls = []
    for vars in itertools.product(attrs["attrs_bra"], attrs["attrs_isic"], attrs["attrs_cbo"]):
        b, i, o = vars
        for u in urls["rais"]:
            if (".show.8" in u and (len(b) == 2 or b == "all")) or ".show.8" not in u:
                formatted_urls.append(u.format(bra=b, isic=i, cbo=o))
    for vars in itertools.product(attrs["attrs_bra"], attrs["attrs_hs"], attrs["attrs_wld"]):
        b, p, w = vars
        for u in urls["secex"]:
            formatted_urls.append(u.format(bra=b, hs=p, wld=w))
            
    return list(formatted_urls)

def add_to_cache(urls):
    count = 0
    ctx = app.test_request_context()
    ctx.push()

    with app.test_client() as c:
        for u in urls:
            count += 1
            print "{0} out of {1} ({2}%)".format(count,len(urls),(round(float(count)/len(urls))*100)), u
            ctx.app.test_client().get(u, headers={'X-Requested-With': 'XMLHttpRequest'})

def main():
    attr_tables = ['attrs_cbo', 'attrs_hs', 'attrs_isic', \
                    'attrs_bra', 'attrs_wld']
    attrs = {attr:get_uniques(attr) for attr in attr_tables}
    
    urls = get_urls()
    urls = format_urls(urls, attrs)
    
    add_to_cache(urls)

if __name__ == "__main__":
    main()