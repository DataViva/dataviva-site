# -*- coding: utf-8 -*-

LocationSelector = {
    "title": "Select a region",
    "selector_url": '/en/wizard/location_selector',
}


ProductSelector = {
    "title": "Select a product",
    "selector_url": '/en/wizard/product_selector',
}


class PathOption:

    def __init__(self, id, title, selectors):
        self.id = id
        self.title = title
        self.selectors = selectors

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "selectors": self.selectors,
        }


class Session:

    def __init__(self, title, options):
        self.title = title
        self.options = options


op1 = PathOption(1, "I want to analysis a product or product category in a given region",
                 selectors=[LocationSelector, ProductSelector])
op2 = PathOption(2, "I want to analysis a product by it's international trading stats",
                 selectors=[ProductSelector, LocationSelector])

entrepreneur_session = Session("What kind of analysis you want to make?", [op1, op2])

SESSIONS = {
    'entrepreneur': entrepreneur_session,
}
