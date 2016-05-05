from re import sub
from jinja2 import Markup
from dataviva.translations.dictionary import dictionary
from dataviva.utils.num_format import num_format
from dataviva.utils.title_case import title_case
from decimal import *
import locale
from flask.ext.babel import gettext

''' A helper class for dealing with injecting times into the page using moment.js'''
class jinja_momentjs:
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def __call__(self, *args):
        return self.format(*args)

    def render(self, format):
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")

class jinja_formatter:
    def __init__(self, text):
        self.text = text

    def __call__(self, *args):
        return self.format(*args)

    @staticmethod
    def is_number(s):
        if s is None:
            return False
        try:
            float(s)
            return True
        except ValueError:
            return False

    def render(self, type):
        if self.is_number(self.text):
            num = float(self.text) if "." in str(self.text) else int(self.text)
            return Markup(num_format(num, type))
        else:
            dict = dictionary()
            if self.text in dict:
                return Markup(dict[self.text])
            else:
                return Markup(title_case(self.text))


''' A helper function for stripping out html tags for showing snippets of user submitted content'''
def jinja_strip_html(s):
    return sub('<[^<]+?>', '', s)

def jinja_split(s, char):
    return s.split(char)

def max_digits(number, digits, monetary=None):

    if type(number) == float :
        number=Decimal(number)

    if type(number) == Decimal:
        if number > 1000:
             number = int(number)
    if number > 1000:
        str_n = [1]
        for i in range(len(str(number)), 0, -3):
            if i > 3:
                str_n.append(0)
                str_n.append(0)
                str_n.append(0)
            else:
                break
        num = int(''.join(map(str, str_n)))
        number = float(number)/num
    number_str = str(number)

    if len(number_str) > 3 and number_str[digits] == '.':
        return number_str[0:digits]
    else:
        return number_str[0:digits+1]

def jinja_magnitude(number):
    if not number: 
        return 0
    integer = str(int(number))
    orders_of_magnitude = ['', gettext('Thousands'), gettext('Millions'), gettext('Billions'), gettext('Trillions')]
    return orders_of_magnitude[len(integer[::3]) - 1]
