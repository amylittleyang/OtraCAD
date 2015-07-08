__author__ = 'jie'
import string
from operator import attrgetter

from cadnano.cnproxy import ProxyObject, ProxySignal
class Domain(ProxyObject):
    def __init__(self,linkedList,low_idx,high_idx,bs_low = None, bs_high = None, hyb_strand=None):
        super(Domain, self).__init__(linkedList)
        self._doc = linkedList.document()
        self._hyb_strand_idx = hyb_strand
        self._index = linkedList._length
        self._vh = linkedList._virtual_helix
        self._vhNum = self._vh._number
        self._name = string.ascii_lowercase[self._index]+str(self._vhNum)     # fix naming
        self._length = high_idx-low_idx +1
        self._sequence = None
        #coordinate of the lowest base
        self._bs_low  = bs_low
        self._bs_high = bs_high
        self._linkedList = linkedList
        self._low_idx = low_idx
        self._high_idx = high_idx
        self._length = high_idx-low_idx+1
        self._domain_3p = None
        self._domain_5p = None
        self._connection_5p = None
        self._connection_3p = None
        self._hyb_domain = None
        self._is_drawn_5_to_3 = self._linkedList.isDrawn5to3()
        if  self._is_drawn_5_to_3:
            self.idx5Prime = self.lowIdx
            self.idx3Prime = self.highIdx
            self.connectionLow = self.connection5p
            self.connectionHigh = self.connection3p
            self.setConnectionLow = self.setConnection5p
            self.setConnectionHigh = self.setConnection3p
        else:
            self.idx5Prime = self.highIdx
            self.idx3Prime = self.lowIdx
            self.connectionLow = self.connection3p
            self.connectionHigh = self.connection5p
            self.setConnectionLow = self.setConnection3p
            self.setConnectionHigh = self.setConnection5p




        cmd = linkedList.createStrand(self,low_idx, high_idx, use_undostack=True)
        if cmd == -1:
            self._oligo = None
            self._strand = None
        else:
            self._strand = cmd._strand
            self._oligo = self._strand._oligo


        if self._hyb_strand_idx > 0:
            self._loop = False
        else:
            self._loop = True

        self.strandUpdateSignal = self._strand.strandUpdateSignal

    def getName(self):
        return self._name

    def oligo(self):
        return self._oligo

    def isStaple(self):
        return self._linkedList._strand_type == 1

    def generator5pStrand(self):
        node0 = node = self
        f = attrgetter('_connection_5p')
        # while node and originalCount == 0:
        #     yield node  # equivalent to: node = node._strand5p
        #     node = f(node)
        #     if node0 == self:
        #         originalCount += 1
        while node:
            yield node  # equivalent to: node = node._strand5p
            node = f(node)
            if node0 == node:
                break


    def generator3pStrand(self):
        node0 = node = self
        f = attrgetter('_connection_3p')
        # while node and originalCount == 0:
        #     yield node  # equivalent to: node = node._strand5p
        #     node = f(node)
        #     if node0 == self:
        #         originalCount += 1
        while node:
            yield node  # equivalent to: node = node._strand5p
            node = f(node)
            if node0 == node:
                break

    def connection3p(self):
        return self._connection_3p

    def connection5p(self):
        return self._connection_5p

    def idxs(self):
        return (self._low_idx, self._high_idx)
    def lowIdx(self):
        return self._low_idx
    # end def

    def highIdx(self):
        return self._high_idx
    # end def

    def strandSet(self):
        return self._linkedList
    def setConnection3p(self, strand):
        self._connection_3p = strand
    # end def

    def setConnection5p(self, strand):
        self._connection_5p = strand
    # end def
    def length(self):
        return self._length
    def virtualHelix(self):
        return self._vh
    def insertionsOnStrand(self):
        return self._strand.insertionsOnStrand()
    def oligo(self):
        return self._oligo
    def document(self):
        return self._doc
    def sequence(self):
        return self._strand.sequence()
    def insertionLengthBetweenIdxs(self, idxL, idxH):
        return self._strand.insertionLengthBetweenIdxs(idxL, idxH)
    def setDomain5p(self,domain):
        self._domain_5p = domain
    def setDomain3p(self,domain):
        self._domain_3p = domain

    def setOligo(self, new_oligo, emit_signal=True):
        self._oligo = new_oligo
        if emit_signal:
            self.strandHasNewOligoSignal.emit(self)

    ### Singals

    strandHasNewOligoSignal = ProxySignal(ProxyObject, name='strandHasNewOligoSignal') #pyqtSignal(QObject)  # strand

    def totalLength(self):
        """
        includes the length of insertions in addition to the bases
        """
        tL = 0
        insertions = self.insertionsOnStrand()

        for insertion in insertions:
            tL += insertion.length()
        return tL + self.length()
    def isScaffold(self):
        return self._linkedList.isScaffold()