from dataviva.api.hedu.models import Yu, Yuc
from dataviva.api.attrs.models import University, Course_hedu
from dataviva import db
from sqlalchemy.sql.expression import func, desc

class UniversityYu:
    def __init__ (self, university_id):
        self.university_id = university_id
        self.yu_max_year_query = db.session.query(func.max(Yu.year)).filter_by(university_id=university_id)
        self.yuc_max_year_query = db.session.query(func.max(Yuc.year))

    def main_info(self):
        yu_query = Yu.query.join(University).filter(Yu.university_id == self.university_id, Yu.year == self.yu_max_year_query)

        yu_data = yu_query.values(
            University.name_pt,
            Yu.enrolled,
            Yu.entrants,
            Yu.graduates,
            Yu.year,
            University.desc_pt
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

    def course_info(self):

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

        course = {}

        for name_pt, enrolled, profile in yuc_enrolled_data:
            course['enrolled_name'] = name_pt
            course['enrolled'] = enrolled
            course['profile'] = profile

        for name_pt, entrants in yuc_entrants_data:
            course['entrants_name'] = name_pt
            course['entrants'] = entrants

        for name_pt, graduates in yuc_graduates_data:
            course['graduates_name'] = name_pt
            course['graduates'] = graduates

        return course