__author__ = 'jie'
from cadnano.cnproxy import ProxyObject, ProxySignal

class LinkedList(ProxyObject):
    def __init__(self, vh):
        super(LinkedList, self).__init__(vh)
        self._virtual_helix = vh
        self._undoStack = None
        self._last_strandset_idx = None
        self._strand_type = strand_type

        self._head = None
        self._next = None

    def append(self,domain):
        # append domian to the end of the list
        if self._head is None:
            self._head = domain
        else:
            curr = self._head
            while curr._next is not None:
                curr = curr._next
            curr._next = domain
    # end def

    def __delete__(self, domain_name):
        # mark domain as inactive, don't delete reference to hybridized domain on scaffold strand
        # retrieve domain by domain_name
        pass

    def insertAt(self,domain,idx):
        # insert domain at specified index. Index numbered 5' to 3'
        pass


