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
from visual import app
from flask import g

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_uniques(table):
    if table == "attrs_bra":
        q = "select bra_id from attrs_yb where length(bra_id) = 8 and population > 100000 and year = 2010;"
    elif table == "attrs_hs":
        q = "select hs_id from secex_yp where length(hs_id) = 6 and val_usd > 100000000 and year = 2010;"
    elif table == "attrs_cbo":
        q = "select cbo_id from rais_yo where length(cbo_id) = 4 and num_emp > 50000 and year = 2010;"
    elif table == "attrs_isic":
        q = "select isic_id from rais_yi where length(isic_id) = 5 and num_emp > 50000 and year = 2010;"
    elif table == "attrs_wld":
        q = "select wld_id from secex_yw where length(wld_id) = 5 and val_usd > 100000000 and year = 2010;"
    else:
        q = "SELECT DISTINCT(id) FROM %s" % (table,)
    cursor.execute(q)
    uniques = [row[0] for row in cursor.fetchall()]
    return uniques

def get_urls():
    urls = {"attrs":[], "rais":[], "secex":[]}
    '''start with attr urls'''
    urls["attrs"] = ['/attrs/cbo/', '/attrs/isic/', '/attrs/hs/', \
                        '/attrs/wld/', '/attrs/bra/']
    
    '''rais'''
    urls["rais"] = ['/rais/all/{bra}/all/show.4/', '/rais/all/{bra}/show.5/all/', \
            '/rais/all/{bra}/{isic}/show.4/', '/rais/all/{bra}/show.5/{cbo}/',
            '/rais/all/{bra}.show.8/all/all/', '/rais/all/{bra}.show.8/{isic}/all/', \
            '/rais/all/{bra}.show.8/all/{cbo}/']
    
    '''secex'''
    urls["secex"] = ['/secex/all/{bra}/all/show.5/', '/secex/all/{bra}/show.6/all/', \
            '/secex/all/{bra}/{hs}/show.5/', '/secex/all/{bra}/show.6/{wld}/',
            '/secex/all/{bra}.show.8/all/all/', '/secex/all/{bra}.show.8/{hs}/all/', \
            '/secex/all/{bra}.show.8/all/{wld}/']
    
    return urls

def format_urls(urls, attrs):
    
    formatted_urls = set(urls["attrs"])
    for vars in itertools.product(attrs["attrs_bra"], attrs["attrs_isic"], attrs["attrs_cbo"]):
        b, i, o = vars
        for u in urls["rais"]:
            formatted_urls.add(u.format(bra=b, isic=i, cbo=o))
    for vars in itertools.product(attrs["attrs_bra"], attrs["attrs_hs"], attrs["attrs_wld"]):
        b, p, w = vars
        for u in urls["secex"]:
            formatted_urls.add(u.format(bra=b, hs=p, wld=w))
    
    return list(formatted_urls)

def add_to_cache(urls):
    count = 0
    ctx = app.test_request_context()
    ctx.push()

    with app.test_client() as c:
        for u in urls:
            count += 1
            print count, u
            ctx.app.test_client().get(u, headers={'X-Requested-With': 'XMLHttpRequest'})

def main():
    attr_tables = ['attrs_cbo', 'attrs_hs', 'attrs_isic', \
                    'attrs_bra', 'attrs_wld']
    attrs = {attr:get_uniques(attr) for attr in attr_tables}
    
    urls = get_urls()
    urls = format_urls(urls, attrs)    
    add_to_cache(urls)
    
    # ctx = app.test_request_context()
    # ctx.push()
    # x = ctx.app.test_client().get('/attrs/hs/', headers={'X-Requested-With': 'XMLHttpRequest'})
    # x = ctx.app.test_client().get('/secex/all/sc050003/show.6/all/', headers={'X-Requested-With': 'XMLHttpRequest'})

if __name__ == "__main__":
    main()