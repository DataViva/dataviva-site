# -*- coding: utf-8 -*-
from dataviva.api.sc.models import Yc_sc, Ysc, Ybc_sc, Ybsc
from dataviva.api.attrs.models import School, Bra, Course_sc
from dataviva import db
from flask import g
from sqlalchemy import func, desc, asc

class Basic_course:
    def __init__(self, course_sc_id):
        self._statistics = None
        self._sc = None

        self.course_sc_id = course_sc_id
        self.max_year_subquery = db.session.query(
            func.max(Yc_sc.year)).filter_by(course_sc_id=course_sc_id)
        self.course_query = Yc_sc.query.join(Course_sc).filter(
                Yc_sc.course_sc_id == self.course_sc_id,
                Yc_sc.year == self.max_year_subquery)

    def __sc__(self):
        if not self._sc:
            sc = self.course_query.first_or_404()
            self._sc = sc
        return self._sc

    def course_name(self):
        course = self.__sc__()
        return course.course_sc.name()

    #def course_description(self):
    #    return self.__statistics__()['course_description']

    def course_classes(self):
        course_classes = self.__sc__()
        return course_classes.classes

    def course_age(self):
        course_age = self.__sc__()
        return course_age.age

    def course_enrolled(self):
        course_enrolled = self.__sc__()
        return course_enrolled.enrolled

    def course_average_class_size(self):
        total_class_number = self.__sc__().classes
        total_enrolled_number = self.__sc__().enrolled

        return total_enrolled_number / total_class_number

    def course_year(self):
        course_year = self.__sc__()
        return course_year.year

    '''def __statistics__(self):

        basic_course = {}

        if self.bra_id:

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

        basic_course['school_count'] = total_schools_query.count()
        basic_course['enrollment_statistics_description'] = 'Enrollment Statistics Description'

        for name_pt, enrolled in school_data:
            basic_course['school_name'] = name_pt
            basic_course['school_enrolled'] = enrolled

        if city_data:
            for name_pt, enrolled in city_data:
                basic_course['city_name'] = name_pt
                basic_course['city_enrolled'] = enrolled
        else:
            basic_course['city_name'] = None
            basic_course['city_enrolled'] = None

        self._statistics = basic_course

        return self._statistics

    def enrollment_statistics_description(self):
        return self.__statistics__()['enrollment_statistics_description']'''

class Basic_course_school(Basic_course):
    def __init__(self, course_sc_id):
        Basic_course.__init__(self, course_sc_id)
        self._sc_count = None
        self.max_year_subquery = db.session.query(
                func.max(Ysc.year)).filter_by(course_sc_id=course_sc_id)
        self._sc_sorted_by_enrollment = None
        self.total_schools_query = Ysc.query.filter(
                    Ysc.course_sc_id == self.course_sc_id,
                    Ysc.year == self.max_year_subquery)

    def __sc_list__(self):
        if not self._sc:
            sc = self.total_schools_query.all()
            self._sc = sc
        return self._sc

    def __sc_count__(self):
        if not self._sc_count:
            sc_count = self.__sc_list__().count()
            self._sc_count = sc_count
        return self._sc_count

    def __sc_sorted_by_enrollment__(self):
        if not self._sc_sorted_by_enrollment:
            self._sc_sorted_by_enrollment = self.__sc_list__()
            self._sc_sorted_by_enrollment.sort(key=lambda sc: sc.enrolled, reverse=True)
        return self._sc_sorted_by_enrollment

    def school_name(self):
        sc = self.__sc_sorted_by_enrollment__()[0]
        return sc.school.name()

    def school_enrolled(self):
        school_enrolled = self.__sc_sorted_by_enrollment__()[0]
        return school_enrolled.enrolled

    def school_count(self):
        school_count = self.total_schools_query.count()
        return school_count

class Basic_course_school_by_location(Basic_course_school):
    def __init__(self, course_sc_id, bra_id):
        Basic_course_school.__init__(self, course_sc_id)
        self.bra_id = bra_id
        self.max_year_subquery = db.session.query(
            func.max(Ybsc.year)).filter_by(course_sc_id=course_sc_id,bra_id=bra_id)
        self.total_schools_query = Ybsc.query.filter(
                Ybsc.course_sc_id == self.course_sc_id,
                Ybsc.year == self.max_year_subquery,
                Ybsc.bra_id == self.bra_id)

'''class Basic_course_city(Basic_course):

    def city_name(self):
        return self.__statistics__()['city_name']

    def city_enrolled(self):
        return self.__statistics__()['city_enrolled']'''

class Basic_course_by_location(Basic_course):
    def __init__(self, course_sc_id, bra_id):
        Basic_course.__init__(self, course_sc_id)
        self.bra_id = bra_id
        self.ybc_max_year_subquery = db.session.query(
            func.max(Ybc_sc.year)).filter_by(course_sc_id=course_sc_id,bra_id=bra_id)
        self.course_query = Ybc_sc.query.join(Course_sc).filter(
                Ybc_sc.course_sc_id == self.course_sc_id,
                Ybc_sc.year == self.ybc_max_year_subquery,
                Ybc_sc.bra_id == self.bra_id)