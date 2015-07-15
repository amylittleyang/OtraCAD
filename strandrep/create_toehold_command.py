__author__ = 'jie'
from cadnano.cnproxy import UndoCommand
class CreateToeholdCommand(UndoCommand):
    def __init__(self,vh,domain,end):
        # domain = domain to operate on
        super(CreateToeholdCommand,self).__init__('create strand')
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
        create new toehold linked list, append toehold to list, linked list has max len 1 for create toehold cmd
        emit signal to notify stranditem for updating appearance(color,toehold item)
        '''





    def undo(self):
        print('undo')
