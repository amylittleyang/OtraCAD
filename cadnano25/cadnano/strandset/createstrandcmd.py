from cadnano.cnproxy import UndoCommand
from cadnano.strand import Strand
from cadnano.oligo import Oligo
import cadnano.preferences as prefs
import random
from strandrep.domain import Domain

class CreateStrandCommand(UndoCommand):
    """
    Create a new Strand based with bounds (base_idx_low, base_idx_high),
    and insert it into the strandset at position strandset_idx. Also,
    create a new Oligo, add it to the Part, and point the new Strand
    at the oligo.
    """
    def __init__(self, strandset, base_idx_low, base_idx_high, strandset_idx):
        super(CreateStrandCommand, self).__init__("create strand")
        self._strandset = strandset
        self._s_set_idx = strandset_idx
        self._domain = Domain(strandset,base_idx_low,base_idx_high)
        colorList = prefs.STAP_COLORS if strandset.isStaple() else prefs.SCAF_COLORS
        color = random.choice(colorList).name()
        self._new_oligo = Oligo(None, color)  # redo will set part
        self._new_oligo.setLength(self._domain.totalLength())
    # end def

    def redo(self):
        # Add the new strand to the StrandSet strand_list
        domain = self._domain
        strandset = self._strandset
        strandset._addToStrandList(domain,self._s_set_idx)
        # Set up the new oligo
        oligo = self._new_oligo
        oligo.setStrand5p(domain)
        oligo.addToPart(strandset.part())
        domain.setOligo(oligo)
        # Emit signal to virtual helix item upon completion
        strandset.strandsetStrandAddedSignal.emit(strandset, domain) #vhitem strandAddedSlot
        # for updating the Slice View displayed helices
        strandset.part().partStrandChangedSignal.emit(strandset.part(), strandset.virtualHelix())
    # end def

    def undo(self):
        # Remove the strand from StrandSet strand_list and selectionList
        strand = self._domain
        strandset = self._domainset
        strandset._doc.removeStrandFromSelection(strand)
        strandset.removeDomainFromStrandList.pop(self._s_set_idx)
        # Get rid of the new oligo
        oligo = self._new_oligo
        oligo.setStrand5p(None)
        oligo.removeFromPart()
        # Emit a signal to notify on completion
        strand.strandRemovedSignal.emit(strand)
        strand.setOligo(None)
        # for updating the Slice View displayed helices
        strandset.part().partStrandChangedSignal.emit(strandset.part(), strandset.virtualHelix())
    # end def
# end class