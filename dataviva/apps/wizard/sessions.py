# -*- coding: utf-8 -*-


class PathOption:

    def __init__(self, id, title, selectors, redirect):
        self.id = id
        self.title = title
        self.selectors = selectors
        self.redirect = redirect

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "selectors": self.selectors,
            "redirect": self.redirect,
        }


class Session:

    def __init__(self, title, options):
        self.title = title
        self.options = options


op1 = PathOption(
    1,
    "I want to analysis a product or product category in a given region",
    selectors=[{"type": "Location", "resp": None},
               {"type": "Product", "resp": None}],
    redirect="/en/path_option_1/bra_id=%s&hs_id=%s"
)

op2 = PathOption(
    2,
    "I want to analysis a product by it's international trading stats",
    selectors=[{"type": "Product", "resp": None},
               {"type": "Location", "resp": None}],
    redirect="/en/path_option_2/hs_id=%s&bra_id=%s"
)

entrepreneur_session = Session(
    "What kind of analysis you want to make?",
    [op1, op2]
)

SESSIONS = {
    'entrepreneur': entrepreneur_session,
    # 'students': students_session,  TODO
    # 'analyst': analyst_session,    TODO
}
