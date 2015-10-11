__author__ = 'jie'
from cadnano.cnproxy import UndoCommand
class PreviewRipOffCommand(UndoCommand):
    '''
    Render operation preview on CustomQGraphicsView, use with undostack
    Push onto undo stack for preview; pop command out of undo stack before applying operation command.
    '''
    def __init__(self,oligo):
        super(PreviewRipOffCommand, self).__init__("preview rip off one oligo")
        self.oligo = oligo
        self.domain5p = oligo.domain5p()

    def redo(self):
        curr = self.domain5p
        while curr is not None:
            curr.togglePreviewRipOffSignal.emit()
            curr = curr.connection3p()

    def undo(self):
        curr = self.domain5p
        while curr is not None:
            curr.togglePreviewRipOffSignal.emit()
            curr = curr.connection3p()