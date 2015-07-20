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

    def setToeholdList(self,toeholdList):
        self._toehold_list = toeholdList

