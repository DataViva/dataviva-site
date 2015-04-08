from re import sub
from jinja2 import Markup
from dataviva.utils.num_format import num_format

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
            return Markup(self.text)


''' A helper funciton for stripping out html tags for showing snippets of user submitted content'''
def jinja_strip_html(s):
    return sub('<[^<]+?>', '', s)

def jinja_split(s, char):
    return s.split(char)
