from decimal import Decimal

''' A Mixin class for retrieving public fields from a model
    and serializing them to a json-compatible object'''
class AutoSerialize(object):
    __public__ = None

    def serialize(self):
        
        data = self.__dict__
        allowed = []
        
        for key, value in data.iteritems():
            
            if isinstance(value,Decimal) or \
                isinstance(value,long):
                value = float(value)
            
            if isinstance(value,unicode) or \
                isinstance(value,float) or \
                isinstance(value,int) or \
                isinstance(value,str):
                allowed.append((key,value))

        data = dict(allowed)
        
        return data
