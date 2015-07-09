__author__ = 'jie'
from cadnano.cnproxy import UndoCommand

class CreateToeholdCommand(UndoCommand):
    def __init__(self,):
        super(CreateToeholdCommand,self).__init__('create strand')

    def redo(self):
        pass
    def undo(self):
        pass
