__author__ = 'jie'
__author__ = 'jie'
TOEHOLD_LENGTH = 5
from cadnano.cnproxy import UndoCommand
from strandrep.toehold_list import ToeholdList
from strandrep.toehold import Toehold
class RemoveToeholdCommand(UndoCommand):
    '''
    called by Domain to create toehold on an end of an oligo;
    can be undone if added to undo stack before executed;
    '''

    def __init__(self,domain,toehold):
        # get references from domain
        super(RemoveToeholdCommand,self).__init__('create strand')
        self._domain = domain
        self._doc = domain._doc
        self._oligo = domain.oligo()
        self._insert_index = None
        self._prime = toehold._prime
        self._toehold = None
        if self._prime == 3:
            self._insert_index = domain.idx3Prime
        else:
            self._insert_index = domain.idx5Prime

    # re-create the toehold and toehold item
    def undo(self):
        # create toehold list as container for toehold domains;
        # add model toehold to toehold list;
        # create toehold item and show item on render view;
        toehold = Toehold(TOEHOLD_LENGTH,self._domain,self._prime) # model toehold
        self._toehold = toehold
        toeholdList = ToeholdList(self._domain,toehold)
        if self._prime == 3:
            self._domain.setToehold3p(toeholdList)
        elif self._prime == 5:
            self._domain.setToehold5p(toeholdList)
        self._domain.toeholdAddedSignal.emit(toehold,self._prime) # emitted by end domain; notifies strand item to create toehold item

    # remove toehold passed in
    #TODO: update domain oligo length
    def redo(self):
        # delete model toehold and toehold item
        if self._prime == 5:
            toeholdList = self._domain.toehold5p()
            toehold_name = 'T5'+self._domain._name
        if self._prime == 3:
            toeholdList = self._domain.toehold3p()
            toehold_name = 'T3'+self._domain._name
        toeholdList.removeToehold(toehold_name)
        # remove toehold item if no toehold remains in toehold list
        if len(toeholdList._toehold_list) == 0:
            if self._prime == 5:
                self._domain.setToehold5p(None)
            if self._prime == 3:
                self._domain.setToehold3p(None)
            self._domain.toeholdRemovedSignal.emit(toeholdList,self._prime) # notifies end domain strand item to hide toehold item



