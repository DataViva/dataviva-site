
def process(depths, attr_type, metric, target_table, year, secex=""):
    if secex:
        secex = " AND month = 0 "

    for depth in depths:
        sql = '''
INSERT INTO attrs_search (SELECT g.{0}_id,  (g.{1} - stats.average) / stats.st AS zvalue, "{0}", (select name_en from attrs_{0} where id=g.{0}_id) as name_en,
 (select name_pt from attrs_{0} where id=g.{0}_id) as name_pt,
 (select color from attrs_{0} where id=g.{0}_id) as color
FROM  {2} g 
CROSS JOIN
(select STDDEV(`{1}`) as st, AVG(`{1}`) as average FROM {2} WHERE {0}_id_len={4} AND year = {3} {5}) stats
WHERE g.{0}_id_len = {4}
AND g.year = {3} {5}
ORDER BY zvalue DESC);
        '''.format(attr_type, metric, target_table, year, depth, secex)

        if attr_type in ["university", "school"]:
            sql = '''
INSERT INTO attrs_search (SELECT g.{0}_id,  (g.{1} - stats.average) / stats.st AS zvalue, "{0}", (select name_en from attrs_{0} where id=g.{0}_id) as name_en,
 (select name_pt from attrs_{0} where id=g.{0}_id) as name_pt,
 (select color from attrs_{0} where id=g.{0}_id) as color
FROM  {2} g 
CROSS JOIN
(select STDDEV(`{1}`) as st, AVG(`{1}`) as average FROM {2} WHERE year = {3} {5}) stats
WHERE g.year = {3} {5}
ORDER BY zvalue DESC);
            '''.format(attr_type, metric, target_table, year, depth, secex)

        print sql 

def process_questions():
    kind = 'learnmore'
    weight = 0
    sql = ''' INSERT INTO attrs_search (SELECT slug, {}, '{}', question, question, '#D67AB0' from ask_question)
    '''.format(weight, kind)
    print sql

# rais
process([1,3,5,7,8,9], "bra", "num_emp", "rais_yb", 2013)
process([1,4], "cbo", "num_emp", "rais_yo", 2013)
process([1, 3, 6], "cnae", "num_emp", "rais_yi", 2013)

# secex
process([2, 6], "hs", "export_val", "secex_ymp", 2013, True)
process([2, 5], "wld", "export_val", "secex_ymw", 2013, True)

# hedu
process([True], "university", "enrolled", "hedu_yu", 2012)
process([6], "course_hedu", "enrolled", "hedu_yc", 2012)

# sc
#### process([True], "school", "enrolled", "sc_ys", 2012)
process([2,5], "course_sc", "enrolled", "sc_yc", 2012)

process_questions()