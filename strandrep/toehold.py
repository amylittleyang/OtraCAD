__author__ = 'jie'
from cadnano.cnproxy import ProxyObject, ProxySignal

class Toehold(ProxyObject):
    '''
    model toehold object; held by toehold list, an attribute of domain
    '''
    def __init__(self,length,domain,prime):
        self._toehold_list = None
        self._length = length
        self._name = 'T' + str(prime) + domain._name
        self._domain = domain
        self._prime = prime
        self._is_drawn_5_to_3 = domain._is_drawn_5_to_3
        self._is_high_idx = False
        if self._is_drawn_5_to_3:
            if self._prime == 3:
                self._is_high_idx = True
        else:
            if self._prime == 5:
                self._is_high_idx = True

    def setToeholdList(self,toeholdList):
        self._toehold_list = toeholdList

    def setLength(self,length):
        self._length = length

    def length(self):
        return self._length