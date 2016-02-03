# -*- coding: utf-8 -*-
from dataviva.api.sc.models import Yc_sc, Ysc, Ybc_sc, Ybsc
from dataviva.api.attrs.models import School, Bra, Course_sc
from dataviva import db
from sqlalchemy import func

class Basic_course:
    def __init__(self, course_sc_id, bra_id):
        self.course_sc_id = course_sc_id
        self.bra_id = bra_id
        self.ybc_max_year_subquery = db.session.query(
            func.max(Ybc_sc.year)).filter_by(course_sc_id=course_sc_id,bra_id=bra_id)
        self.ybsc_max_year_subquery = db.session.query(
            func.max(Ybsc.year)).filter_by(course_sc_id=course_sc_id,bra_id=bra_id)

    def statistics(self):

        course = {}

        course_query = Ybc_sc.query.join(Course_sc).filter(
            Ybc_sc.course_sc_id == self.course_sc_id,
            Ybc_sc.year == self.ybc_max_year_subquery,
            Ybc_sc.bra_id == self.bra_id)

        total_schools_query = Ybsc.query.filter(
            Ybsc.course_sc_id == self.course_sc_id,
            Ybsc.year == self.ybsc_max_year_subquery,
            Ybsc.bra_id == self.bra_id)

        most_enrolled_school_query = Ybsc.query.join(School).filter(
            Ybsc.course_sc_id == self.course_sc_id,
            Ybsc.year == self.ybsc_max_year_subquery,
            Ybsc.bra_id == self.bra_id) \
            .order_by(Ybsc.enrolled.desc()).limit(1)

        most_enrolled_city_query = Ybc_sc.query.join(Bra).filter(
            Ybc_sc.course_sc_id == self.course_sc_id,
            Ybc_sc.year == self.ybc_max_year_subquery,
            Ybc_sc.bra_id.like(str(self.bra_id)+'%'),
            Ybc_sc.bra_id_len == 9) \
            .order_by(Ybc_sc.enrolled.desc()).limit(1)
     
        course_data = course_query.values(Course_sc.name_pt,
                                    Course_sc.desc_pt,
                                    Ybc_sc.classes,
                                    Ybc_sc.age,
                                    Ybc_sc.enrolled,
                                    Ybc_sc.year)

        school_data = most_enrolled_school_query.values(School.name_pt,
                                                       Ybsc.enrolled)

        if len(self.bra_id) < 9:
            city_data = most_enrolled_city_query.values(
                Bra.name_pt,
                Ybc_sc.enrolled)
        else:
            city_data = None

        for name_pt, desc_pt, classes, age, enrolled, year in course_data:
            course['course_name'] = name_pt
            course['course_description'] = desc_pt or unicode('Não há descrição para este curso.', 'utf8')
            course['course_classes'] = classes
            course['course_age'] = age
            course['course_enrolled'] = enrolled
            course['course_average_class_size'] = enrolled / classes
            course['course_year'] = year

        course['schools_count'] = total_schools_query.count()    

        for name_pt, enrolled in school_data:
            course['school_name'] = name_pt
            course['school_enrolled'] = enrolled

        if city_data:
            for name_pt, enrolled in city_data:
                course['city_name'] = name_pt
                course['city_enrolled'] = enrolled

        return course