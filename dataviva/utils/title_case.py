import re

''' Titlecase Function '''
def title_case(string):
    if not string:
        return ""
    elif not isinstance(string, (unicode, str)):
        return string

    exceptions = ['a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'from', 'if', \
              'in', 'into', 'near', 'nor', 'of', 'on', 'onto', 'or', 'that', \
              'the', 'to', 'with', 'via', 'vs', 'vs.', 'per', \
              'um', 'uma', 'e', 'como', 'em', 'no', 'na', 'mas', 'por', \
              'para', 'pelo', 'pela', 'de', 'do', 'da', 'se', 'perto', 'nem', \
              'ou', 'que', 'o', 'a', 'com']
    uppers = ["ID", "CEO", "CEOs", "CFO", "CFOs", "CNC", "COO", "COOs", "CPU", "HVAC", "GDP", "GINI", "IDHM", "R&D", "P&D", "PIB", "IT", "TI", "TV", "UI"]
    smalls = [s.lower() for s in uppers]

    words = re.split('(\s|-|\/|\()', string)

    def detect_string(s, i):
        if i != 0 and s.lower() in exceptions:
            return s.lower()
        elif s.lower() in smalls:
            return uppers[smalls.index(s.lower())]
        else:
            return s.capitalize()

    for i, word in enumerate(words):
        words[i] = detect_string(word, i)

    return "".join(words)
