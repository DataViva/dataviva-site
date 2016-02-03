from dataviva.api.hedu.models import Yu, Yuc, Yc_hedu, Ybc_hedu
from dataviva.api.attrs.models import University as uni, Course_hedu, Bra
from dataviva import db
from sqlalchemy.sql.expression import func, desc

class University:
    def __init__ (self, university_id):
        self.university_id = university_id
        self.yu_max_year_query = db.session.query(func.max(Yu.year)).filter_by(university_id=university_id)
        self.yuc_max_year_query = db.session.query(func.max(Yuc.year))

    def university_info(self):
        yu_query = Yu.query.join(uni).filter(Yu.university_id == self.university_id, Yu.year == self.yu_max_year_query)

        yu_data = yu_query.values(
            uni.name_pt,
            Yu.enrolled,
            Yu.entrants,
            Yu.graduates,
            Yu.year,
            uni.desc_pt
        )

        university = {}

        for name_pt, enrolled, entrants, graduates, year, profile in yu_data:
            university['name'] = name_pt
            university['enrolled'] = enrolled
            university['entrants'] = entrants
            university['graduates'] =  graduates
            university['profile'] = profile
            university['year'] =  year

        return university

    def majors_with_more_enrollments(self):

        yuc_enrolled_query = Yuc.query.join(Course_hedu).filter(
            Yuc.university_id == self.university_id,
            Yuc.year == self.yuc_max_year_query,
            func.length(Yuc.course_hedu_id) == 6).order_by(desc(Yuc.enrolled)).limit(1)

        yuc_entrants_query = Yuc.query.join(Course_hedu).filter(
            Yuc.university_id == self.university_id,
            Yuc.year == self.yuc_max_year_query,
            func.length(Yuc.course_hedu_id) == 6).order_by(desc(Yuc.entrants)).limit(1)

        yuc_graduates_query = Yuc.query.join(Course_hedu).filter(
            Yuc.university_id == self.university_id,
            Yuc.year == self.yuc_max_year_query,
            func.length(Yuc.course_hedu_id) == 6).order_by(desc(Yuc.graduates)).limit(1)

        yuc_enrolled_data = yuc_enrolled_query.values(
            Course_hedu.name_pt,
            Yuc.enrolled,
            Course_hedu.desc_pt
        )

        yuc_entrants_data = yuc_entrants_query.values(
            Course_hedu.name_pt,
            Yuc.entrants
        )

        yuc_graduates_data = yuc_graduates_query.values(
            Course_hedu.name_pt,
            Yuc.graduates
        )

        major = {}

        for name_pt, enrolled, profile in yuc_enrolled_data:
            major['enrolled_name'] = name_pt
            major['enrolled'] = enrolled
            major['profile'] = profile

        for name_pt, entrants in yuc_entrants_data:
            major['entrants_name'] = name_pt
            major['entrants'] = entrants

        for name_pt, graduates in yuc_graduates_data:
            major['graduates_name'] = name_pt
            major['graduates'] = graduates

        return major

class Major:
    def __init__ (self, course_hedu_id):
        self.course_hedu_id = course_hedu_id
        self.yc_max_year_query = db.session.query(func.max(Yc_hedu.year))
        self.yuc_max_year_query = db.session.query(func.max(Yuc.year))
        self.ybc_max_year_query = db.session.query(func.max(Ybc_hedu.year))

    def major_info(self):
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

        return major

    def university_and_county_with_more_enrollments(self):
        yuc_enrolled_query = Yuc.query.join(uni).filter(
            Yuc.course_hedu_id == self.course_hedu_id,
            Yuc.year == self.yuc_max_year_query
        ).order_by(desc(Yuc.enrolled)).limit(1)

        ybc_enrolled_query =  Ybc_hedu.query.join(Bra).filter(
            Ybc_hedu.course_hedu_id == self.course_hedu_id,
            Ybc_hedu.year == self.ybc_max_year_query,
            func.length(Ybc_hedu.bra_id) == 9
        ).order_by(desc(Ybc_hedu.enrolled)).limit(1)

        yuc_entrants_query = Yuc.query.join(uni).filter(
            Yuc.course_hedu_id == self.course_hedu_id,
            Yuc.year == self.yuc_max_year_query
        ).order_by(desc(Yuc.entrants)).limit(1)

        ybc_entrants_query =  Ybc_hedu.query.join(Bra).filter(
            Ybc_hedu.course_hedu_id == self.course_hedu_id,
            Ybc_hedu.year == self.ybc_max_year_query,
            func.length(Ybc_hedu.bra_id) == 9
        ).order_by(desc(Ybc_hedu.entrants)).limit(1)

        yuc_graduates_query = Yuc.query.join(uni).filter(
            Yuc.course_hedu_id == self.course_hedu_id,
            Yuc.year == self.yuc_max_year_query
        ).order_by(desc(Yuc.graduates)).limit(1)

        ybc_graduates_query =  Ybc_hedu.query.join(Bra).filter(
            Ybc_hedu.course_hedu_id == self.course_hedu_id,
            Ybc_hedu.year == self.ybc_max_year_query,
            func.length(Ybc_hedu.bra_id) == 9
        ).order_by(desc(Ybc_hedu.graduates)).limit(1)

        yuc_enrolled_data = yuc_enrolled_query.values(
            uni.name_pt,
            Course_hedu.desc_pt,
            Yuc.enrolled
        )

        ybc_enrolled_data = ybc_enrolled_query.values(
            Bra.name_pt,
            Ybc_hedu.enrolled
        )

        yuc_entrants_data = yuc_entrants_query.values(
            uni.name_pt,
            Yuc.entrants
        )

        ybc_entrants_data = ybc_entrants_query.values(
            Bra.name_pt,
            Ybc_hedu.entrants
        )

        yuc_graduates_data = yuc_graduates_query.values(
            uni.name_pt,
            Yuc.graduates
        )

        ybc_graduates_data = ybc_graduates_query.values(
            Bra.name_pt,
            Ybc_hedu.graduates
        )
        
        enrollments = {}

        for name_pt, desc_pt, enrolled in yuc_enrolled_data:
            enrollments['enrolled_university'] = name_pt
            enrollments['profile'] = desc_pt
            enrollments['enrolled_university_data'] = enrolled

        for name_pt, enrolled in ybc_enrolled_data:
            enrollments['enrolled_county'] = name_pt
            enrollments['enrolled_county_data'] = enrolled

        for name_pt, entrants in yuc_entrants_data:
            enrollments['entrants_university'] = name_pt
            enrollments['entrants_university_data'] = entrants

        for name_pt, entrants in ybc_entrants_data:
            enrollments['entrants_county'] = name_pt
            enrollments['entrants_county_data'] = entrants    

        for name_pt, graduates in yuc_graduates_data:
            enrollments['graduates_university'] = name_pt
            enrollments['graduates_university_data'] = graduates

        for name_pt, graduates in ybc_graduates_data:
            enrollments['graduates_county'] = name_pt
            enrollments['graduates_county_data'] = graduates

        return enrollments

