# -*- coding: utf-8 -*-
from dataviva.api.sc.models import Yc_sc, Ysc, Ybc_sc, Ybsc
from dataviva.api.attrs.models import School, Bra, Course_sc
from dataviva import db
from sqlalchemy import func

class Basic_course:
    def __init__(self, course_sc_id, bra_id):
        self._statistics = None
        
        self.course_sc_id = course_sc_id
        self.bra_id = bra_id
        self.ybc_max_year_subquery = db.session.query(
            func.max(Ybc_sc.year)).filter_by(course_sc_id=course_sc_id,bra_id=bra_id)
        self.ybsc_max_year_subquery = db.session.query(
            func.max(Ybsc.year)).filter_by(course_sc_id=course_sc_id,bra_id=bra_id)
        self.yc_max_year_subquery = db.session.query(
            func.max(Yc_sc.year)).filter_by(course_sc_id=course_sc_id)
        self.ysc_max_year_subquery = db.session.query(
                func.max(Ysc.year)).filter_by(course_sc_id=course_sc_id)

    def __statistics__(self):

        basic_course = {}

        if self.bra_id:

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

            school_data = most_enrolled_school_query.values(
                School.name_pt,
                Ybsc.enrolled)

            if len(self.bra_id) < 9:
                city_data = most_enrolled_city_query.values(
                    Bra.name_pt,
                    Ybc_sc.enrolled)
            else:
                city_data = None

        else:

            course_query = Yc_sc.query.join(Course_sc).filter(
                Yc_sc.course_sc_id == self.course_sc_id,
                Yc_sc.year == self.yc_max_year_subquery)

            total_schools_query = Ysc.query.filter(
                Ysc.course_sc_id == self.course_sc_id,
                Ysc.year == self.ysc_max_year_subquery)
            
            most_enrolled_school_query = Ysc.query.join(School).filter(
                Ysc.course_sc_id == self.course_sc_id,
                Ysc.year == self.ysc_max_year_subquery) \
                .order_by(Ysc.enrolled.asc())

            most_enrolled_city_query = Ybc_sc.query.join(Bra).filter(
                Ybc_sc.course_sc_id == self.course_sc_id,
                Ybc_sc.year == self.ysc_max_year_subquery,
                Ybc_sc.bra_id_len == 9) \
                .order_by(Ybc_sc.enrolled.asc())

            course_data = course_query.values(
                Course_sc.name_pt,
                Course_sc.desc_pt,
                Yc_sc.classes,
                Yc_sc.age,
                Yc_sc.enrolled,
                Yc_sc.year)

            school_data = most_enrolled_school_query.values(
                School.name_pt,
                Ysc.enrolled)

            city_data = most_enrolled_city_query.values(
                Bra.name_pt,
                Ybc_sc.enrolled)

        for name_pt, desc_pt, classes, age, enrolled, year in course_data:
            basic_course['course_name'] = name_pt
            basic_course['course_description'] = desc_pt or unicode('Não há descrição para este curso.', 'utf8')
            basic_course['course_classes'] = classes
            basic_course['course_age'] = age
            basic_course['course_enrolled'] = enrolled
            basic_course['course_year'] = year

        basic_course['schools_count'] = total_schools_query.count()
        basic_course['enrollment_statistics_description'] = 'Enrollment Statistics Description'

        for name_pt, enrolled in school_data:
            basic_course['school_name'] = name_pt
            basic_course['school_enrolled'] = enrolled

        if city_data:
            for name_pt, enrolled in city_data:
                basic_course['city_name'] = name_pt
                basic_course['city_enrolled'] = enrolled

        self._statistics = basic_course

        return self._statistics

    def course_name(self):
        return self.__statistics__()['course_name']

    def course_description(self):
        return self.__statistics__()['course_description']

    def course_classes(self):
        return self.__statistics__()['course_classes']

    def course_age(self):
        return self.__statistics__()['course_age']

    def course_enrolled(self):
        return self.__statistics__()['course_enrolled']

    def course_average_class_size(self):
        total_class_number = self.__statistics__()['course_classes']
        total_enrolled_number = self.__statistics__()['course_enrolled']

        return total_enrolled_number / total_class_number
    
    def course_year(self):
        return self.__statistics__()['course_year']
    
    def schools_count(self):
        return self.__statistics__()['schools_count']

    def enrollment_statistics_description(self):
        return self.__statistics__()['enrollment_statistics_description']

    def school_name(self):
        return self.__statistics__()['school_name']

    def school_enrolled(self):
        return self.__statistics__()['school_enrolled']

    def city_name(self):
        return self.__statistics__()['city_name']

    def city_enrolled(self):
        return self.__statistics__()['city_enrolled']