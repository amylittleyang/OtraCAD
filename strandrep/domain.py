__author__ = 'jie'
import string
class Domain:
    def __init__(self,vhNum, domain_idx, bs_low = None, bs_high = None, hyb_strand=None):
        self._hyb_strand_idx = hyb_strand
        self._index = domain_idx
        self._vhNum = vhNum
        self._name = string.ascii_lowercase[domain_idx]+str(vhNum)     # fix naming
#        self._length = bs_high-bs_low +1
        self._sequence = None
        self._bs_low  = bs_low
        self._bs_high = bs_high

        self._next = None
        self._hyb_domain = None

        if self._hyb_strand > 0:
            self._loop = False
        else:
            self._loop = True

    def getName(self):
        return self._name




