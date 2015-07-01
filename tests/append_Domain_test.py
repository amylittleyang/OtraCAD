__author__ = 'jie'
from strandrep.domain import Domain
from strandrep.linked_list import LinkedList
from cadnano.enum import StrandType
from cadnano.virtualhelix import VirtualHelix

def appendDomain(list,hyb_stap,strand_linkedList,idx,low):
    if idx == len(list) or len(list) == 0:
        domain = Domain(strand_linkedList,low,low+idx-1,bs_low=list[0],bs_high=list[len(list)-1],hyb_strand=hyb_stap)
        strand_linkedList.append(domain)
        return
    now_stap = list[idx][4]
    if now_stap != hyb_stap:
#        print(strand_linkedList._length)
        domain = Domain(strand_linkedList,low,low+idx-1,bs_low=list[0],bs_high=list[idx-1],hyb_strand=hyb_stap)
        strand_linkedList.append(domain)
        low = low + idx
        appendDomain(list[idx:],now_stap,strand_linkedList,0,low)
    else:
        appendDomain(list,hyb_stap,strand_linkedList,idx+1,low)




if __name__ == '__main__':
    scaf_linkedList = LinkedList(StrandType.OVERHANG,10)
    list = [[10,0,0,0,-1],[2,0,0,0,-1],[2,0,0,0,1],[200,0,0,0,1],[20,0,0,0,2]]
    hyb_stap = list[0][4]
    appendDomain(list, hyb_stap,scaf_linkedList,0,0)
    curr = scaf_linkedList._head
    while True:
        print ('domain idx %d low base %d, high base %d, low index %d, high index %d, hybridized to staple number %d.' % (curr._index,curr._bs_low[0],curr._bs_high[0],curr._low_idx,curr._high_idx,curr._hyb_strand_idx))
        curr = curr._next
        if curr == None:
            break
