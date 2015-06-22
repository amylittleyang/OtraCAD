__author__ = 'jie'
import string
class Domain:
    def __init__(self,hybridized, vhNum, domain_Idx, bs_low = None, bs_high = None):
        self._hybridized = hybridized
        self._vhNum = vhNum
        self._name = string.ascii_lowercase[domain_Idx]+vhNum
        self._length = bs_high-bs_low +1
        self._sequence = None

        if self._hybridized_:
            self._loop = False
        else:
            self._loop = True




