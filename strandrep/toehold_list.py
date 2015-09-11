__author__ = 'jie'
from strandrep.toehold_item import ToeholdItem
from cadnano.cnproxy import ProxySignal,ProxyObject
class ToeholdList(ProxyObject):
    def __init__(self,domain,toehold):
        '''
        container for all toehold domains on one end of an oligo
        has at least one toehold upon initialization;
        can convert domain into toehold, vice versa;
        upon deletion of head toehold, remove toehold item, restore domain._toehold(which prime) to None
        '''
        super(ToeholdList, self).__init__()
        self._domain = domain
        self._toehold_list = []
        self._toehold_list.append(toehold)
        self._length = 1
        self._base_length = toehold._length
        self._is_high_idx = toehold._is_high_idx
        self._is_drawn_5_to_3 = self._domain._is_drawn_5_to_3

    toeholdRemovedFromSelectionSignal = ProxySignal(ProxyObject,name='toeholdRemovedFromSelectionSignal') #connect to toehold_item
    toeholdSelectedSignal = ProxySignal(ProxyObject,name='toeholdSelectedSignal')#connect to toehold_item

    def append(self,toehold):
        '''
        don't call append to add the first toehold object
        pass first toehold object as argument to the initialization function
        '''
        self._toehold_list.append(toehold)

    def removeToehold(self,toehold_name):
        # remove model toehold
        for t in self._toehold_list:
            if t._name == toehold_name:
                self._toehold_list.remove(t)