__author__ = 'jie'
from cadnano.cnproxy import UndoCommand
class CreateToeholdCommand(UndoCommand):
    def __init__(self,vh,domain,end):
        super(CreateToeholdCommand,self).__init__('create strand')
        self._overhang_linkedlist = vh._overhang_LinkedList
        self._domain = domain
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
        '''
        create new toehold domain
        add toehold to correct connection on domain;
        insert toehold at correct location on overhangLinkedlist
        emit signal to notify virtualhelixitem for updating render(color,toehold item)
        '''
        from domain import Domain
        idx = self._insert_index()
        if self._overhang_linkedlist._is_Drawn_5_to_3:
            if self._prime == 5:
                toehold = Domain(self._overhang_linkedlist,idx-5,idx)

            elif self._prime == 3:
                toehold = Domain(self._overhang_linkedlist,idx,idx+5)
        else:
            if self._prime == 5:
                toehold = Domain(self._overhang_linkedlist,idx,idx+5)

            elif self._prime == 3:
                toehold = Domain(self._overhang_linkedlist,idx-5,idx)
        self._toehold = toehold
        self._overhang_linkedlist.append(toehold)
        if self._prime == 3:
            self._domain.setConnection3p(toehold)
            self._domain.setToehold3p(toehold)
            toehold.setConnection5p(self._domain)
        else:
            self._domain.setConnection5p(toehold)
            self._domain.setToehold5p(toehold)
            toehold.setConnection3p(self._domain)

        self._overhang_linkedlist.finishAppend()


    def undo(self):
        print('undo')
        if self._prime == 3:
            toehold = self._domain.toehold3p()
        else:
            toehold = self._domain.toehold5p()
        #TODO: code removeToehold() in linked_list; need removeToeholdCommand for undo stack
        # self._overhang_linkedlist.removeDomainAt(toehold._index)
        if toehold is None:
            return
        self._overhang_linkedlist.removeStrand(toehold._strand,toehold._linkedList)
        if self._prime == 3:
            toehold.setConnection5p(None)
            self._domain.setConnection3p(None)
            self._domain.setToehold3p(None)
        else:
            toehold.setConnection3p(None)
            self._domain.setConnection5p(None)
            self._domain.setToehold5p(None)