__author__ = 'jie'
from cadnano.cnproxy import UndoCommand
from strandrep.toehold_list import ToeholdList
from strandrep.toehold import Toehold
class CreateToeholdCommand(UndoCommand):
    def __init__(self,vh,domain,end):
        # domain = domain to operate on
        super(CreateToeholdCommand,self).__init__('create strand')
        self._domain = domain
        self._overhang_linkedlist = vh._overhang_LinkedList
        self._doc = domain._doc
        self._oligo = domain.oligo()
        self._insert_index = None
        self._prime = end
        self._toehold = None
        if end == 3:
            self._insert_index = domain.idx3Prime
        else:
            self._insert_index = domain.idx5Prime

    def redo(self):
        print('redo')
        #TODO: substitute 5 with user length input
        toehold = Toehold(5,self._domain,self._prime)
        self._toehold = toehold
        toeholdList = ToeholdList(self._domain,toehold)
        if self._prime == 3:
            self._domain.setToehold3p(toeholdList)
        elif self._prime == 5:
            self._domain.setToehold5p(toeholdList)
        self._domain.toeholdAddedSignal.emit(self._domain,self._prime)

    #     #TODO: update domain oligo length
    def undo(self):
        print('undo')
        if self._prime == 5:
            toeholdList = self._domain.toehold5p()
            toehold_name = 'T5'+self._domain._name
        if self._prime == 3:
            toeholdList = self._domain.toehold3p()
            toehold_name = 'T3'+self._domain._name
        toeholdList.removeToehold(toehold_name)
        if len(toeholdList._toehold_list) == 0:
            if self._prime == 5:
                self._domain.setToehold5p(None)
            if self._prime == 3:
                self._domain.setToehold3p(None)
            self._domain.toeholdRemovedSignal.emit(self._domain,self._prime )



