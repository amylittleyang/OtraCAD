__author__ = 'jie'
from strandrep.toehold_item import ToeholdItem
from cadnano.cnproxy import ProxySignal,ProxyObject
class ToeholdList(ProxyObject):
    def __init__(self,domain,toehold):
        '''
        has at least one toehold in initialization;
        controls toehold item;
        can convert domain into toehold, vice versa;
        upon deletion of head toehold, remove toehold item, restore domain._toehold(which prime) to None
        '''
        super(ToeholdList, self).__init__()
        self._domain = domain
        self._toehold_list = []
        self._toehold_list.append(toehold)
        self._length = 1
        self._base_length = toehold._length


    def append(self,toehold):
        '''
        don't call append to add the first toehold object
        pass first toehold object as argument to the initialization function
        '''
        self._toehold_list.append(toehold)
    def removeLast(self):
        self._toehold_list.pop(-1)