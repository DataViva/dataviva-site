from dataviva import db
from flask import g
from dataviva.utils.title_case import title_case


class BasicAttr(object):
    name_en = db.Column(db.String(200))
    name_pt = db.Column(db.String(200))
    color = db.Column(db.String(7))
    gender_pt = db.Column(db.String(1))
    plural_pt = db.Column(db.Boolean())
    article_pt = db.Column(db.Boolean())

    def name(self):
        lang = getattr(g, "locale", "en")
        return title_case(getattr(self, "name_"+lang))

    def preposition(self, preposition):
        if g.locale == "en":
            if preposition == 'de':
                return 'of'
            elif preposition == 'em':
                return 'in'
        else:
            if self.article_pt:
                if preposition == 'de':
                    contraction = {
                        'f': 'da',
                        'm': 'do',
                    }
                elif preposition == 'em':
                    contraction = {
                        'f': 'na',
                        'm': 'no',
                    }
                return contraction[self.gender_pt] + ('s' if self.plural_pt else '')
            else:
                return preposition

    def article(self):
        if self.article_pt:
            if self.gender_pt == 'm':
                return 'o' + ('s' if self.plural_pt else '')
            else:
                return 'a' + ('s' if self.plural_pt else '')
        else:
            return ''


class ExpandedAttr(BasicAttr):
    desc_en = db.Column(db.Text())
    desc_pt = db.Column(db.Text())
    keywords_en = db.Column(db.String(100))
    keywords_pt = db.Column(db.String(100))
