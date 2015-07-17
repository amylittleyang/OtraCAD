__author__ = 'jie'
from cadnano.cnproxy import ProxyObject, ProxySignal

class Toehold(ProxyObject):
    def __init__(self,length,domain):
        self._toehold_list = None
        self._length = length
        self._name = 'T' + domain._name
        self._domain = domain

    def setToeholdList(self,toeholdList):
        self._toehold_list = toeholdList

