from dataviva.api.hedu.models import Yu, Yuc, Yc_hedu, Ybc_hedu
from dataviva.api.attrs.models import University as uni, Course_hedu, Bra
from dataviva import db
from sqlalchemy.sql.expression import func, desc


class University:
    def __init__(self, university_id):
        self._hedu = None
        self._hedu_sorted_by_enrolled = None
        self._hedu_sorted_by_entrants = None
        self._hedu_sorted_by_graduates = None

        self.university_id = university_id
        self.max_year_query = db.session.query(func.max(Yu.year)).filter_by(university_id=university_id)
        self.hedu_query = Yu.query.join(uni).filter(
            Yu.university_id == self.university_id, 
            Yu.year == self.max_year_query)

    def __hedu__(self):
        if not self._hedu:
            hedu_data = self.hedu_query.first_or_404()
            self._hedu = hedu_data
        return self._hedu

    def __hedu_list__(self):
        if not self._hedu:
            hedu_data = self.hedu_query.all()
            self._hedu = hedu_data
        return self._hedu

    def __hedu_sorted_by_enrolled__(self):
        self._hedu_sorted_by_enrolled = self.__hedu_list__()
        self._hedu_sorted_by_enrolled.sort(key=lambda hedu: hedu.enrolled, reverse=True)
        return self._hedu_sorted_by_enrolled

    def __hedu_sorted_by_entrants__(self):
        self._hedu_sorted_by_entrants = self.__hedu_list__()
        self._hedu_sorted_by_entrants.sort(key=lambda hedu: hedu.entrants, reverse=True)
        return self._hedu_sorted_by_entrants

    def __hedu_sorted_by_graduates__(self):
        self._hedu_sorted_by_graduates = self.__hedu_list__()
        self._hedu_sorted_by_graduates.sort(key=lambda hedu: hedu.graduates, reverse=True)
        return self._hedu_sorted_by_graduates

    def name(self):
        return self.__hedu__().university.name()

    def enrolled(self):
        return self.__hedu__().enrolled

    def entrants(self):
        return self.__hedu__().entrants

    def graduates(self):
        return self.__hedu__().graduates

    def profile(self):
        return self.__hedu__().university.desc_pt

    def year(self):
        return self.__hedu__().year

    def highest_enrolled_number(self):
        hedu = self.__hedu_sorted_by_enrolled__()[0]
        return hedu.enrolled

    def highest_entrants_number(self):
        hedu = self.__hedu_sorted_by_entrants__()[0]
        return hedu.entrants

    def highest_graduates_number(self):
        hedu = self.__hedu_sorted_by_graduates__()[0]
        return hedu.graduates

class UniversityMajors(University):

    def __init__(self, university_id):
        University.__init__(self, university_id)
        self.max_year_query = db.session.query(func.max(Yuc.year))
        self.hedu_query = Yuc.query.join(uni).join(Course_hedu).filter(
            Yuc.university_id == self.university_id,
            Yuc.year == self.max_year_query,
            func.length(Yuc.course_hedu_id) == 6)

    def major_with_more_enrollments(self):
        hedu = self.__hedu_sorted_by_enrolled__()[0]
        return hedu.course_hedu.name()

    def major_with_more_entrants(self):
        hedu = self.__hedu_sorted_by_entrants__()[0]
        return hedu.course_hedu.name()

    def major_with_more_graduates(self):
        hedu = self.__hedu_sorted_by_graduates__()[0]
        return hedu.course_hedu.name()


class Major:
    def __init__(self, course_hedu_id):
        self._hedu = None
        self.course_hedu_id = course_hedu_id

        self.max_year_query = db.session.query(func.max(Yc_hedu.year)).filter_by(course_hedu_id=course_hedu_id)

        self.hedu_query = Yc_hedu.query.join(Course_hedu).filter(
            Yc_hedu.course_hedu_id == self.course_hedu_id, 
            Yc_hedu.year == self.max_year_query)

    def __hedu__(self):
        if not self._hedu:
            hedu_data = self.hedu_query.one()
            self._hedu = hedu_data

        return self._hedu

    def name(self):
        return self.__hedu__().course_hedu.name()

    def enrolled(self):
        return self.__hedu__().enrolled

    def entrants(self):
        return self.__hedu__().entrants

    def graduates(self):
        return self.__hedu__().graduates

    def profile(self):
        return self.__hedu__().course_hedu.desc_pt

    def year(self):
        return self.__hedu__().year

    
class EnrolledByUniversity(Major):
    def __init__(self, course_hedu_id):
        self._hedu = None
        self.course_hedu_id = course_hedu_id

        self.max_year_query = db.session.query(func.max(Yuc.year)).filter_by(course_hedu_id=course_hedu_id)
        self.hedu_query = Yuc.query.join(uni).filter(
            Yuc.course_hedu_id == self.course_hedu_id,
            Yuc.year == self.max_year_query
        ).order_by(desc(Yuc.enrolled)).limit(1)

    def university_with_more_enrolled(self):
        return self.__hedu__().university.name()

    def highest_enrolled_number_by_university(self):
        return self.__hedu__().enrolled


class EnrolledByMunicipality(Major):
    def __init__(self, course_hedu_id):
        self._hedu = None
        self.course_hedu_id = course_hedu_id

        self.max_year_query = db.session.query(func.max(Ybc_hedu.year)).filter_by(course_hedu_id=course_hedu_id)

        self.hedu_query =  Ybc_hedu.query.join(Bra).filter(
            Ybc_hedu.course_hedu_id == self.course_hedu_id,
            Ybc_hedu.year == self.max_year_query,
            func.length(Ybc_hedu.bra_id) == 9
        ).order_by(desc(Ybc_hedu.enrolled)).limit(1)


    def municipality_with_more_enrolled(self):
        return self.__hedu__().bra

    def highest_enrolled_number_by_municipality(self):
        return self.__hedu__().enrolled
        
class EntrantsByUniversity(Major):
    def __init__(self, course_hedu_id):
        self._hedu = None
        self.course_hedu_id = course_hedu_id

        self.max_year_query = db.session.query(func.max(Yuc.year)).filter_by(course_hedu_id=course_hedu_id)
        self.hedu_query = Yuc.query.join(uni).filter(
            Yuc.course_hedu_id == self.course_hedu_id,
            Yuc.year == self.max_year_query
        ).order_by(desc(Yuc.entrants)).limit(1)

    def university_with_more_entrants(self):
        return self.__hedu__().university.name()

    def highest_entrant_number_by_university(self):
        return self.__hedu__().entrants


class EntrantsByMunicipality(Major):
    def __init__(self, course_hedu_id):
        self._hedu = None
        self.course_hedu_id = course_hedu_id

        self.max_year_query = db.session.query(func.max(Ybc_hedu.year)).filter_by(course_hedu_id=course_hedu_id)

        self.hedu_query =  Ybc_hedu.query.join(Bra).filter(
            Ybc_hedu.course_hedu_id == self.course_hedu_id,
            Ybc_hedu.year == self.max_year_query,
            func.length(Ybc_hedu.bra_id) == 9
        ).order_by(desc(Ybc_hedu.entrants)).limit(1)


    def municipality_with_more_entrants(self):
        return self.__hedu__().bra.name()

    def highest_entrant_number_by_municipality(self):
        return self.__hedu__().entrants

class GraduatesByUniversity(Major):
    def __init__(self, course_hedu_id):
        self._hedu = None
        self.course_hedu_id = course_hedu_id

        self.max_year_query = db.session.query(func.max(Yuc.year)).filter_by(course_hedu_id=course_hedu_id)
        self.hedu_query = Yuc.query.join(uni).filter(
            Yuc.course_hedu_id == self.course_hedu_id,
            Yuc.year == self.max_year_query
        ).order_by(desc(Yuc.graduates)).limit(1)

    def university_with_more_graduates(self):
        return self.__hedu__().university.name()

    def highest_graduate_number_by_university(self):
        return self.__hedu__().graduates


class GraduatesByMunicipality(Major):
    def __init__(self, course_hedu_id):
        self._hedu = None
        self.course_hedu_id = course_hedu_id

        self.max_year_query = db.session.query(func.max(Ybc_hedu.year)).filter_by(course_hedu_id=course_hedu_id)

        self.hedu_query =  Ybc_hedu.query.join(Bra).filter(
            Ybc_hedu.course_hedu_id == self.course_hedu_id,
            Ybc_hedu.year == self.max_year_query,
            func.length(Ybc_hedu.bra_id) == 9
        ).order_by(desc(Ybc_hedu.graduates)).limit(1)


    def municipality_with_more_graduates(self):
        return self.__hedu__().bra.name()

    def highest_graduate_number_by_municipality(self):
        return self.__hedu__().graduates
