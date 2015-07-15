__author__ = 'jie'
from strandrep.toehold_item import ToeholdItem
class ToeholdList(object):
    def __init__(self,domain,toehold):
        '''
        has at least one toehold in initialization;
        controls toehold item;
        can convert domain into toehold, vice versa;
        upon deletion of head toehold, remove toehold item, restore domain._toehold(which prime) to None
        '''
        self._domain = domain
        self._toehold_list = []
        self._toehold_list.append(toehold)
        self._length = 1
        self._base_length = toehold._length
        self._toehold_item = ToeholdItem()

    def append(self,toehold):
        '''
        don't call append to add the first toehold object
        pass first toehold object as argument to the initialization function
        '''
        self._toehold_list.append(toehold)

