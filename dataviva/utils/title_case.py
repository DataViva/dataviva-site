import re

''' Titlecase Function '''
def title_case(string):
    if not string:
      return ""

    exceptions = ['A', 'An', 'And', 'As', 'At', 'But', 'By', 'For', 'From', 'If', \
              'In', 'Into', 'Near', 'Nor', 'Of', 'On', 'Onto', 'Or', 'That', \
              'The', 'To', 'With', 'Via', 'Vs', 'Vs.', \
              'Um', 'Uma', 'E', 'Como', 'Em', 'No', 'Na', 'Mas', 'Por', \
              'Para', 'Pelo', 'Pela', 'De', 'Do', 'Da', 'Se', 'Perto', 'Nem', \
              'Ou', 'Que', 'O', 'A', 'Com']
    uppers = ['Id', 'Tv', 'R&d', "P&d", "It", "Ti"]
    words = re.split('(\s|-|\/|\()', string)
    def detect_string(s):
        if s in exceptions or s.capitalize() in exceptions:
            return s.lower()
        elif s in uppers or s.capitalize() in uppers:
            return s.upper()
        else:
            return s.capitalize()
    
    for i, word in enumerate(words):
        words[i] = detect_string(word)
        
    words[0] = words[0].capitalize()
    
    return "".join(words)

