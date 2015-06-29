__author__ = 'jie'
import string
class Domain:
    def __init__(self,linkedList,low_idx,high_idx,bs_low = None, bs_high = None, hyb_strand=None):
        self._hyb_strand_idx = hyb_strand
        self._index = linkedList._length
        self._vh = linkedList._virtual_helix
        self._name = string.ascii_lowercase[self._index]+str(self._vh)     # fix naming
#        self._length = bs_high-bs_low +1
        self._sequence = None
        self._bs_low  = bs_low
        self._bs_high = bs_high
        self._linkedList = linkedList
        self._low_idx = low_idx
        self._high_idx = high_idx

        self._next = None
        self._hyb_domain = None
        cmd = linkedList.createStrand(low_idx, high_idx, use_undostack=True)
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

    def getName(self):
        return self._name

    def oligo(self):
        return self._oligo

    def isStaple(self):
        return self._linkedList._strand_type == 1




