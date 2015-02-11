# -*- coding: utf-8 -*-
from dictionary import dictionary

''' Translates the columns names
'''
def translate(column):

    d = dictionary()
    return d.get(column, column)
