from dataviva.api.hedu.models import Ybu, Ybc_hedu, Yu, Yuc, Yc_hedu, Ybuc
from dataviva.api.attrs.models import University as uni, Course_hedu, Bra
from dataviva import db
from sqlalchemy.sql.expression import func, desc, not_


class University:

    def __init__(self, university_id):
        self._hedu = None
        self._hedu_sorted_by_enrolled = None
        self._hedu_sorted_by_entrants = None
        self._hedu_sorted_by_graduates = None
        self.university_id = university_id

        if university_id is None:
            self.max_year_query = db.session.query(func.max(Yu.year))
            self.hedu_query = Yu.query.filter(Yu.year == self.max_year_query)
        else:
            self.max_year_query = db.session.query(
                func.max(Yu.year)).filter_by(university_id=university_id)
            self.hedu_query = Yu.query.filter(
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
        if not self._hedu_sorted_by_enrolled:
            self._hedu_sorted_by_enrolled = self.__hedu_list__()
            self._hedu_sorted_by_enrolled.sort(
                key=lambda hedu: hedu.enrolled, reverse=True)
        return self._hedu_sorted_by_enrolled

    def __hedu_sorted_by_entrants__(self):
        if not self._hedu_sorted_by_entrants:
            self._hedu_sorted_by_entrants = self.__hedu_list__()
            self._hedu_sorted_by_entrants.sort(
                key=lambda hedu: hedu.entrants, reverse=True)
        return self._hedu_sorted_by_entrants

    def __hedu_sorted_by_graduates__(self):
        if not self._hedu_sorted_by_graduates:
            self._hedu_sorted_by_graduates = self.__hedu_list__()
            self._hedu_sorted_by_graduates.sort(
                key=lambda hedu: hedu.graduates, reverse=True)
        return self._hedu_sorted_by_graduates

    def name(self):
        return self.__hedu__().university.name()

    def university_type(self):
        return self.__hedu__().university.school_type()

    def enrolled(self):
        return self.__hedu__().enrolled

    def entrants(self):
        return self.__hedu__().entrants

    def graduates(self):
        return self.__hedu__().graduates

    def profile(self):
        return self.__hedu__().university.desc_pt

    def year(self):
        return self.max_year_query.first()[0]

    def highest_enrolled_number(self):
        hedu = self.__hedu_sorted_by_enrolled__()[0]
        return hedu.enrolled

    def highest_entrants_number(self):
        hedu = self.__hedu_sorted_by_entrants__()[0]
        return hedu.entrants

    def highest_graduates_number(self):
        hedu = self.__hedu_sorted_by_graduates__()[0]
        return hedu.graduates

    def highest_enrolled_by_university(self):
        hedu_list = self.__hedu_sorted_by_enrolled__()
        if len(hedu_list) != 0:
            hedu = hedu_list[0]
            return hedu.enrolled
        else:
            return None

    def highest_enrolled_by_university_name(self):
        hedu_list = self.__hedu_sorted_by_enrolled__()
        if len(hedu_list) != 0:
            hedu = hedu_list[0]
            return hedu.university.name()
        else:
            return None


class UniversityMajors(University):

    def __init__(self, university_id):
        University.__init__(self, university_id)
        self.max_year_query = db.session.query(func.max(Yuc.year))
        self.hedu_query = Yuc.query.filter(
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

    def __init__(self, course_hedu_id, bra_id):
        self._hedu = None
        self._hedu_sorted_by_enrolled = None
        self._hedu_sorted_by_entrants = None
        self._hedu_sorted_by_graduates = None
        self._hedu_major_rank = None

        self.course_hedu_id = course_hedu_id
        self.bra_id = bra_id

        if course_hedu_id is None and bra_id is None:
           self.max_year_query = db.session.query(func.max(Yc_hedu.year))
           self.hedu_query = Ybc_hedu.query.filter(Ybc_hedu.year == self.max_year_query)
        else:
            self.max_year_query = db.session.query(
                func.max(Yc_hedu.year)).filter_by(course_hedu_id=course_hedu_id)

            if bra_id != '':
                self.hedu_query = Ybc_hedu.query.filter(
                    Ybc_hedu.course_hedu_id == self.course_hedu_id,
                    Ybc_hedu.bra_id == self.bra_id,
                    Ybc_hedu.year == self.max_year_query)
            else:
                self.hedu_query = Yc_hedu.query.filter(
                    Yc_hedu.course_hedu_id == self.course_hedu_id,
                    Yc_hedu.year == self.max_year_query)

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
        if not self._hedu_sorted_by_enrolled:
            self._hedu_sorted_by_enrolled = self.__hedu_list__()
            self._hedu_sorted_by_enrolled.sort(
                key=lambda hedu: hedu.enrolled, reverse=True)
        return self._hedu_sorted_by_enrolled

    def __hedu_sorted_by_entrants__(self):
        if not self._hedu_sorted_by_entrants:
            self._hedu_sorted_by_entrants = self.__hedu_list__()
            self._hedu_sorted_by_entrants.sort(
                key=lambda hedu: hedu.entrants, reverse=True)
        return self._hedu_sorted_by_entrants

    def __hedu_sorted_by_graduates__(self):
        if not self._hedu_sorted_by_graduates:
            self._hedu_sorted_by_graduates = self.__hedu_list__()
            self._hedu_sorted_by_graduates.sort(
                key=lambda hedu: hedu.graduates, reverse=True)
        return self._hedu_sorted_by_graduates

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

    def highest_enrolled_number(self):
        hedu = self.__hedu_sorted_by_enrolled__()[0]
        return hedu.enrolled

    def highest_entrants_number(self):
        hedu = self.__hedu_sorted_by_entrants__()[0]
        return hedu.entrants

    def highest_graduates_number(self):
        hedu = self.__hedu_sorted_by_graduates__()[0]
        return hedu.graduates

    def location_name(self):
        return Bra.query.filter(Bra.id == self.bra_id).first().name()

    def highest_enrolled_by_major(self):
        hedu_list = self.__hedu_sorted_by_enrolled__()
        if len(hedu_list) != 0:
            hedu = hedu_list[0]
            return hedu.enrolled
        else:
            return None

    def highest_enrolled_by_major_name(self):
        hedu_list = self.__hedu_sorted_by_enrolled__()
        if len(hedu_list) != 0:
            hedu = hedu_list[0]
            return hedu.course_hedu.name()
        else:
            return None


class MajorUniversities(Major):

    def __init__(self, course_hedu_id, bra_id):
        Major.__init__(self, course_hedu_id, bra_id)
        self.course_hedu_id = course_hedu_id

        self.max_year_query = db.session.query(
            func.max(Yuc.year)).filter_by(course_hedu_id=course_hedu_id)
        if bra_id == '':
            self.hedu_query = Yuc.query.filter(
                Yuc.course_hedu_id == self.course_hedu_id,
                Yuc.year == self.max_year_query)
        else:
            self.hedu_query = Ybuc.query.filter(
                Ybuc.course_hedu_id == self.course_hedu_id,
                Ybuc.bra_id == self.bra_id,
                Ybuc.year == self.max_year_query)

    def university_with_more_enrolled(self):
        hedu = self.__hedu_sorted_by_enrolled__()[0]
        return hedu.university.name()

    def university_with_more_entrants(self):
        hedu = self.__hedu_sorted_by_entrants__()[0]
        return hedu.university.name()

    def university_with_more_graduates(self):
        hedu = self.__hedu_sorted_by_graduates__()[0]
        return hedu.university.name()


class MajorMunicipalities(Major):

    def __init__(self, course_hedu_id, bra_id):
        Major.__init__(self, course_hedu_id, bra_id)
        self.course_hedu_id = course_hedu_id

        self.max_year_query = db.session.query(
            func.max(Ybc_hedu.year)).filter_by(course_hedu_id=course_hedu_id)

        if bra_id == '':
            self.hedu_query = Ybc_hedu.query.filter(
                Ybc_hedu.course_hedu_id == self.course_hedu_id,
                Ybc_hedu.year == self.max_year_query,
                not_(Ybc_hedu.bra_id.like('0xx%')),
                func.length(Ybc_hedu.bra_id) == 9)
        else:
            self.hedu_query = Ybc_hedu.query.filter(
                Ybc_hedu.course_hedu_id == self.course_hedu_id,
                Ybc_hedu.year == self.max_year_query,
                Ybc_hedu.bra_id.like(self.bra_id+'%'),
                not_(Ybc_hedu.bra_id.like('0xx%')),
                func.length(Ybc_hedu.bra_id) == 9)

    def municipality_with_more_enrolled(self):
        hedu = self.__hedu_sorted_by_enrolled__()[0]
        return hedu.bra.name()

    def municipality_with_more_enrolled_state(self):
        hedu = self.__hedu_sorted_by_enrolled__()[0]
        return hedu.bra.abbreviation

    def municipality_with_more_entrants(self):
        hedu = self.__hedu_sorted_by_entrants__()[0]
        return hedu.bra.name()

    def municipality_with_more_entrants_state(self):
        hedu = self.__hedu_sorted_by_entrants__()[0]
        return hedu.bra.abbreviation

    def municipality_with_more_graduates(self):
        hedu = self.__hedu_sorted_by_graduates__()[0]
        return hedu.bra.name()

    def municipality_with_more_graduates_state(self):
        hedu = self.__hedu_sorted_by_graduates__()[0]
        return hedu.bra.abbreviation


class LocationUniversity:

    def __init__(self, bra_id):
        self._hedu_sorted_by_enrolled = None
        self._hedu = None
        self.bra_id = bra_id
        self.max_year_query = db.session.query(
            func.max(Ybu.year)).filter_by(bra_id=bra_id)
        self.hedu_query = Ybu.query.join(uni).filter(
            Ybu.bra_id == self.bra_id,
            Ybu.year == self.max_year_query)

    def __hedu__(self):
        if not self._hedu:
            hedu_data = self.hedu_query.one()
            self._hedu = hedu_data
        return self._hedu

    def __hedu_list__(self):
        if not self._hedu:
            hedu_data = self.hedu_query.all()
            self._hedu = hedu_data
        return self._hedu

    def __hedu_sorted_by_enrolled__(self):
        if not self._hedu_sorted_by_enrolled:
            self._hedu_sorted_by_enrolled = self.__hedu_list__()
            self._hedu_sorted_by_enrolled.sort(
                key=lambda hedu: hedu.enrolled, reverse=True)
        return self._hedu_sorted_by_enrolled

    def year(self):
        return self.max_year_query.first()[0]

    def highest_enrolled_by_university(self):
        hedu_list = self.__hedu_sorted_by_enrolled__()
        if len(hedu_list) != 0:
            hedu = hedu_list[0]
            return hedu.enrolled
        else:
            return None

    def highest_enrolled_by_university_name(self):
        hedu_list = self.__hedu_sorted_by_enrolled__()
        if len(hedu_list) != 0:
            hedu = hedu_list[0]
            return hedu.university.name()
        else:
            return None


class LocationMajor(LocationUniversity):

    def __init__(self, bra_id):
        LocationUniversity.__init__(self, bra_id)
        self._hedu = None
        self.bra_id = bra_id
        self.max_year_query = db.session.query(
            func.max(Ybc_hedu.year)).filter_by(bra_id=bra_id)
        self.hedu_query = Ybc_hedu.query.join(Course_hedu).filter(
            Ybc_hedu.bra_id == self.bra_id,
            Ybc_hedu.course_hedu_id_len == 6,
            Ybc_hedu.year == self.max_year_query)

    def highest_enrolled_by_major(self):
        hedu_list = self.__hedu_sorted_by_enrolled__()
        if len(hedu_list) != 0:
            hedu = hedu_list[0]
            return hedu.enrolled
        else:
            return None

    def highest_enrolled_by_major_name(self):
        hedu_list = self.__hedu_sorted_by_enrolled__()
        if len(hedu_list) != 0:
            hedu = hedu_list[0]
            return hedu.course_hedu.name()
        else:
            return None
