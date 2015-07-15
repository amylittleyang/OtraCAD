__author__ = 'jie'
from cadnano.cnproxy import ProxyObject, ProxySignal

class Toehold(ProxyObject):
    def __init__(self,toeholdList,length):
        self._toehold_list = toeholdList
        self._length = length

