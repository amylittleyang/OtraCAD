#!/usr/bin/env python
# encoding: utf-8

from cadnano.cnproxy import ProxyObject, ProxySignal
import cadnano.util as util
from cadnano.enum import StrandType

from cadnano.cnproxy import UndoStack, UndoCommand

from cadnano.strandset import StrandSet

from .removevhelixcmd import RemoveVirtualHelixCommand
from strandrep.linked_list import LinkedList
class VirtualHelix(ProxyObject):
    """
    VirtualHelix is a container class for two StrandSet objects (one scaffold
    and one staple). The Strands all share the same helix axis. It is called
    "virtual" because many different Strands (i.e. sub-oligos) combine to
    form the "helix", just as many fibers may be braided together to 
    form a length of rope.
    """

    def __init__(self, part, row, col, idnum=0):
        self._doc = part.document()
        super(VirtualHelix, self).__init__(part)
        self._coord = (row, col) # col, row
        self._part = part
        self._scaf_LinkedList = LinkedList(StrandType.SCAFFOLD, self)
        self._stap_LinkedList = LinkedList(StrandType.STAPLE, self)
        self._overHang_LinkedList = LinkedList(StrandType.OVERHANG,self)
        # If self._part exists, it owns self._number
        # in that only it may modify it through the
        # private interface. The public interface for
        # setNumber just routes the call to the parent
        # dnapart if one is present. If self._part == None
        # the virtualhelix owns self._number and may modify it.
        self._number = None
        self.setNumber(idnum)
    # end def

    def __repr__(self):
        return "<%s(%d)>" % (self.__class__.__name__, self._number)

    ### SIGNALS ###
    virtualHelixRemovedSignal = ProxySignal(ProxyObject, name='virtualHelixRemovedSignal')  #pyqtSignal(QObject)  # self
    virtualHelixNumberChangedSignal = ProxySignal(ProxyObject, int, name='virtualHelixNumberChangedSignal') #pyqtSignal(QObject, int)  # self, num

    ### SLOTS ###

    ### ACCESSORS ###
    def scaf(self, idx):
        """ Returns the strand at idx in self's scaffold, if any """
        return self._scaf_LinkedList.domainAtIndex(idx)

    def stap(self, idx):
        """ Returns the strand at idx in self's scaffold, if any """
        return self._stap_LinkedList.domainAtIndex(idx)

    def coord(self):
        return self._coord
    # end def

    def number(self):
        return self._number
    # end def

    def part(self):
        return self._part
    # end def
    
    def document(self):
        return self._doc
    # end def
    
    def setNumber(self, number):
        if self._number != number:
            num_to_vh_dict = self._part._number_to_virtual_helix
            # if self._number is not None:
            num_to_vh_dict[self._number] = None
            self._number = number
            self.virtualHelixNumberChangedSignal.emit(self, number)
            num_to_vh_dict[number] = self
    # end def

    def setPart(self, new_part):
        self._part = new_part
        self.setParent(new_part)
    # end def

    def scaffoldStrandSet(self):
        return self._scaf_LinkedList
    # end def

    def stapleStrandSet(self):
        return self._stap_LinkedList
    # end def

    def undoStack(self):
        return self._part.undoStack()
    # end def

    ### METHODS FOR QUERYING THE MODEL ###
    def scaffoldIsOnTop(self):
        return self.isEvenParity()

    def getStrandSetByIdx(self, idx):
        """
        This is a path-view-specific accessor
        idx == 0 means top strand
        idx == 1 means bottom strand
        """
        if idx == 0:
            if self.isEvenParity():
                return self._scaf_LinkedList
            else:
                return self._stap_LinkedList
        else:
            if self.isEvenParity():
                return self._stap_LinkedList
            else:
                return self._scaf_LinkedList
    # end def

    def getStrandSetByType(self, strand_type):
        if strand_type == StrandType.SCAFFOLD:
            return self._scaf_LinkedList
        elif strand_type == StrandType.STAPLE:
            return self._stap_LinkedList
        else:
            return self._overHang_LinkedList
    # end def

    def getStrandSets(self):
        """Return a tuple of the scaffold and staple StrandSets."""
        return self._scaf_LinkedList, self._stap_LinkedList, self._overHang_LinkedList
    # end def

    def hasStrandAtIdx(self, idx):
        """Return a tuple for (Scaffold, Staple). True if
           a strand is present at idx, False otherwise."""
        return (self._scaf_LinkedList.hasStrandAt(idx, idx),\
                self._stap_LinkedList.hasStrandAt(idx, idx),\
                self._overHang_LinkedList.hasStrandAt(idx,idx))
    # end def

    def indexOfRightmostNonemptyBase(self):
        """Returns the rightmost nonempty base in either scaf of stap."""
        return max(self._scaf_LinkedList.indexOfRightmostNonemptyBase(),\
                   self._stap_LinkedList.indexOfRightmostNonemptyBase())
    # end def

    def isDrawn5to3(self, strandset):
        is_scaf = strandset == self._scaf_LinkedList
        is_even = self.isEvenParity()
        return is_even == is_scaf
    # end def

    def isEvenParity(self):
        return self._part.isEvenParity(*self._coord)
    # end def

    def strandSetBounds(self, idx_helix, idx_type):
        """
        forwards the query to the strandset
        """
        return self.strandSet(idx_helix, idx_type).bounds()
    # end def

    ### METHODS FOR EDITING THE MODEL ###
    def destroy(self):
        # QObject also emits a destroyed() Signal
        self.setParent(None)
        self.deleteLater()
    # end def
    
    def remove(self, use_undostack=True):
        """
        Removes a VirtualHelix from the model. Accepts a reference to the 
        VirtualHelix, or a (row,col) lattice coordinate to perform a lookup.
        """
        if use_undostack:
            self.undoStack().beginMacro("Delete VirtualHelix")
        self._scaf_LinkedList.remove(use_undostack)
        self._stap_LinkedList.remove(use_undostack)
        c = RemoveVirtualHelixCommand(self.part(), self)
        if use_undostack:
            self.undoStack().push(c)
            self.undoStack().endMacro()
        else:
            c.redo()
    # end def

    ### PUBLIC SUPPORT METHODS ###
    def deepCopy(self, part):
        """
        This only copies as deep as the VirtualHelix
        strands get copied at the oligo and added to the Virtual Helix
        """
        vh = VirtualHelix(part, self._number)
        vh._coords = (self._coord[0], self._coord[1])
        # If self._part exists, it owns self._number
        # in that only it may modify it through the
        # private interface. The public interface for
        # setNumber just routes the call to the parent
        # dnapart if one is present. If self._part == None
        # the virtualhelix owns self._number and may modify it.
        self._number = idnum
    # end def

    def getLegacyStrandSetArray(self, strand_type):
        """Called by legacyencoder."""
        if strand_type == StrandType.SCAFFOLD:
            return self._scaf_LinkedList.getLegacyArray()
        elif strand_type == StrandType.STAPLE:
            return self._stap_LinkedList.getLegacyArray()
        else:
            return self._overHang_LinkedList.getLegacyArray()

    def shallowCopy(self):
        pass
    # end def

    # def translateCoords(self, deltaCoords):
    #     """
    #     for expanding a helix
    #     """
    #     deltaRow, deltaCol = deltaCoords
    #     row, col = self._coord
    #     self._coord = row + deltaRow, col + deltaCol
    # # end def

# end class