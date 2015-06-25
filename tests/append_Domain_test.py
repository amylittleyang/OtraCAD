__author__ = 'jie'
from strandrep.domain import Domain
from strandrep.linked_list import LinkedList
from cadnano.enum import StrandType
from cadnano.virtualhelix import VirtualHelix

def appendDomain(list,hyb_stap,scaf_linkedList,idx,domain_idx):
    if idx == len(list) or len(list) == 0:
        domain = Domain(scaf_linkedList._virtual_helix, domain_idx ,bs_low=list[0],bs_high=list[len(list)-1],hyb_strand=hyb_stap)
        scaf_linkedList.append(domain)
        domain_idx+=1
        return
    now_stap = list[idx][4]
    if now_stap != hyb_stap:
        domain = Domain(scaf_linkedList._virtual_helix, domain_idx ,bs_low=list[0],bs_high=list[idx-1],hyb_strand=hyb_stap)
        scaf_linkedList.append(domain)
        domain_idx+=1
        appendDomain(list[idx:],now_stap,scaf_linkedList,0,domain_idx)
    else:
        appendDomain(list,hyb_stap,scaf_linkedList,idx+1,domain_idx)



if __name__ == '__main__':
    scaf_linkedList = LinkedList(StrandType.OVERHANG,10)
    list = [[10,0,0,0,-1],[2,0,0,0,-1],[2,0,0,0,1],[200,0,0,0,1],[20,0,0,0,2]]
    hyb_stap = list[0][4]
    appendDomain(list, hyb_stap,scaf_linkedList,0,0)
    curr = scaf_linkedList._head
    while True:
        print 'domain idx %d low base %d, high base %d, hybridized to staple number %d on helix number %d' % (curr._idx,curr._bs_low[0],curr._bs_high[0],curr._hyb_strand,curr._vhNum)
        curr = curr._next
        if curr == None:
            break
