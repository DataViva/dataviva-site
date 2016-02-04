from dataviva.api.hedu.models import Yu, Yuc, Yc_hedu, Ybc_hedu
from dataviva.api.attrs.models import University as uni, Course_hedu, Bra
from dataviva import db
from sqlalchemy.sql.expression import func, desc


class University:
    def __init__(self, university_id):
        self._hedu = None
        self.university_id = university_id

        self.max_year_query = db.session.query(func.max(Yu.year)).filter_by(university_id=university_id)

        self.hedu_query = Yu.query.join(uni).filter(
            Yu.university_id == self.university_id, 
            Yu.year == self.max_year_query)

    def __hedu__(self):
        if not self._hedu:
            hedu_data = self.hedu_query.one()
            self._hedu = hedu_data

        return self._hedu

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

class UniversityMajorByEnrollments(University):

    def __init__(self, university_id):
        University.__init__(self, university_id)
        self.max_year_query = db.session.query(func.max(Yuc.year))
        self.hedu_query = Yuc.query.join(Course_hedu).filter(
            Yuc.university_id == self.university_id,
            Yuc.year == self.max_year_query,
            func.length(Yuc.course_hedu_id) == 6).order_by(desc(Yuc.enrolled)).limit(1)

    def major_with_more_enrollments(self):
        return self.__hedu__().course_hedu.name()

    def highest_enrollment_number_by_major(self):
        return self.__hedu__().enrolled

class UniversityMajorByEntrants(University):

    def __init__(self, university_id):
        University.__init__(self, university_id)
        self.max_year_query = db.session.query(func.max(Yuc.year))
        self.hedu_query = Yuc.query.join(Course_hedu).filter(
            Yuc.university_id == self.university_id,
            Yuc.year == self.max_year_query,
            func.length(Yuc.course_hedu_id) == 6).order_by(desc(Yuc.entrants)).limit(1)

    def major_with_more_entrants(self):
        return self.__hedu__().course_hedu.name()

    def highest_entrant_number_by_major(self):
        return self.__hedu__().entrants

class UniversityMajorByGraduates(University):
    def __init__(self, university_id):
        University.__init__(self, university_id)
        self.max_year_query = db.session.query(func.max(Yuc.year))
        self.hedu_query = Yuc.query.join(Course_hedu).filter(
            Yuc.university_id == self.university_id,
            Yuc.year == self.max_year_query,
            func.length(Yuc.course_hedu_id) == 6).order_by(desc(Yuc.graduates)).limit(1)

    def major_with_more_graduates(self):
        return self.__hedu__().course_hedu.name()

    def highest_graduate_number_by_major(self):
        return self.__hedu__().graduates


class Major:
    def __init__ (self, course_hedu_id):

        self._major = None

        self.course_hedu_id = course_hedu_id
        self.yc_max_year_query = db.session.query(func.max(Yc_hedu.year))
        self.yuc_max_year_query = db.session.query(func.max(Yuc.year))
        self.ybc_max_year_query = db.session.query(func.max(Ybc_hedu.year))

    def __major_info__(self):
        if not self._major:
            yc_query = Yc_hedu.query.join(Course_hedu).filter(
                Yc_hedu.course_hedu_id == self.course_hedu_id,
                Yc_hedu.year == self.yc_max_year_query
            )

            yc_data = yc_query.values(
                Course_hedu.name_pt,
                Course_hedu.desc_pt,
                Yc_hedu.year,
                Yc_hedu.enrolled,
                Yc_hedu.entrants,
                Yc_hedu.graduates
            )

            major = {}

            for name_pt, desc_pt, year, enrolled, entrants, graduates in yc_data:
                major['name'] = name_pt
                major['profile'] = desc_pt
                major['year'] = year
                major['enrolled'] = enrolled
                major['entrants'] = entrants
                major['graduates'] = graduates

            self._major = major

        return self._major

    def name(self):
        return self.__major_info__()['name']

    def enrolled(self):
        return self.__major_info__()['enrolled']

    def entrants(self):
        return self.__major_info__()['entrants']

    def graduates(self):
        return self.__major_info__()['graduates']

    def profile(self):
        return self.__major_info__()['profile']

    def year(self):
        return self.__major_info__()['year']

    def university_with_more_enrolled(self):
        yuc_enrolled_query = Yuc.query.join(uni).filter(
            Yuc.course_hedu_id == self.course_hedu_id,
            Yuc.year == self.yuc_max_year_query
        ).order_by(desc(Yuc.enrolled)).limit(1)

        yuc_enrolled_data = yuc_enrolled_query.values(
            uni.name_pt,
            Course_hedu.desc_pt,
            Yuc.enrolled
        )

        university = {}

        for name_pt, desc_pt, enrolled in yuc_enrolled_data:
            university['name'] = name_pt
            university['profile'] = desc_pt
            university['value'] = enrolled

        return university

    def municipality_with_more_enrolled(self):
        ybc_enrolled_query =  Ybc_hedu.query.join(Bra).filter(
            Ybc_hedu.course_hedu_id == self.course_hedu_id,
            Ybc_hedu.year == self.ybc_max_year_query,
            func.length(Ybc_hedu.bra_id) == 9
        ).order_by(desc(Ybc_hedu.enrolled)).limit(1)

        ybc_enrolled_data = ybc_enrolled_query.values(
            Bra.name_pt,
            Ybc_hedu.enrolled
        )

        municipality = {}

        for name_pt, enrolled in ybc_enrolled_data:
            municipality['name'] = name_pt
            municipality['value'] = enrolled

        return municipality

    def university_with_more_entrants(self):
        yuc_entrants_query = Yuc.query.join(uni).filter(
            Yuc.course_hedu_id == self.course_hedu_id,
            Yuc.year == self.yuc_max_year_query
        ).order_by(desc(Yuc.entrants)).limit(1)

        yuc_entrants_data = yuc_entrants_query.values(
            uni.name_pt,
            Yuc.entrants
        )

        university = {}

        for name_pt, entrants in yuc_entrants_data:
            university['name'] = name_pt
            university['value'] = entrants

        return university

    def municipality_with_more_entrants(self):
        ybc_entrants_query =  Ybc_hedu.query.join(Bra).filter(
            Ybc_hedu.course_hedu_id == self.course_hedu_id,
            Ybc_hedu.year == self.ybc_max_year_query,
            func.length(Ybc_hedu.bra_id) == 9
        ).order_by(desc(Ybc_hedu.entrants)).limit(1)

        ybc_entrants_data = ybc_entrants_query.values(
            Bra.name_pt,
            Ybc_hedu.entrants
        )

        municipality = {}

        for name_pt, entrants in ybc_entrants_data:
            municipality['name'] = name_pt
            municipality['value'] = entrants

        return municipality

    def university_with_more_graduates(self):
        yuc_graduates_query = Yuc.query.join(uni).filter(
            Yuc.course_hedu_id == self.course_hedu_id,
            Yuc.year == self.yuc_max_year_query
        ).order_by(desc(Yuc.graduates)).limit(1)

        yuc_graduates_data = yuc_graduates_query.values(
            uni.name_pt,
            Yuc.graduates
        )

        university = {}

        for name_pt, graduates in yuc_graduates_data:
            university['name'] = name_pt
            university['value'] = graduates

        return university

    def municipality_with_more_graduates(self):
        ybc_graduates_query =  Ybc_hedu.query.join(Bra).filter(
            Ybc_hedu.course_hedu_id == self.course_hedu_id,
            Ybc_hedu.year == self.ybc_max_year_query,
            func.length(Ybc_hedu.bra_id) == 9
        ).order_by(desc(Ybc_hedu.graduates)).limit(1)

        ybc_graduates_data = ybc_graduates_query.values(
            Bra.name_pt,
            Ybc_hedu.graduates
        )
        
        municipality = {}  

        for name_pt, graduates in ybc_graduates_data:
            municipality['name'] = name_pt
            municipality['value'] = graduates

        return municipality

