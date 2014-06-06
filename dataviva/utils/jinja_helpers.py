from re import sub
from jinja2 import Markup

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
        
    def render(self, type, lang):
        if isinstance(self.text,unicode) or isinstance(self.text,str):
            format = "text"
        else:
            format = "number"
            
        return Markup("<script>\ndocument.write(dataviva.format.%s(\"%s\",\"%s\",\"%s\"))\n</script>" % (format, self.text, type, str(lang)))

''' A helper funciton for stripping out html tags for showing snippets of user submitted content'''
def jinja_strip_html(s):
    return sub('<[^<]+?>', '', s)

def jinja_split(s, char):
    return s.split(char)
