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
        toehold = Domain(self._overhang_linkedlist,idx,idx+8)
        self._toehold = toehold
        self._overhang_linkedlist.append(toehold)
        if self._prime == 3:
            self._domain.setConnection3p(toehold)
            toehold.setConnection5p(self._domain)
        else:
            self._domain.setConnection5p(toehold)
            toehold.setConnection3p(self._domain)

    def undo(self):
        if self._prime == 3:
            self._domain.setConnection3p(None)
            self._toehold.setConnection5p(None)
        else:
            self._domain.setConnection5p(None)
            self._toehold.setConnection3p(None)
        print(self._toehold._name)
        #TODO: code removeToehold() in linked_list; need removeToeholdCommand for undo stack
        self._overhang_linkedlist.removeDomainAt(self._toehold._index)
        self._toehold = None
