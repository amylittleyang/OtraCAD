__author__ = 'jie'
from strandrep.domain import Domain
from strandrep.linked_list import LinkedList
def appendDomain(list,hyb_stap,scaf_linkedList,idx,domain_idx):
    if idx == len(list) or len(list) == 0:
        domain = Domain(hyb_stap!=-1,scaf_linkedList._virtual_helix, domain_idx ,bs_low=list[0],bs_high=list[len(list)-1])
        scaf_linkedList.append(domain)
        domain_idx+=1
        return
    now_stap = list[idx][4]
    if now_stap != hyb_stap:
        domain = Domain(hyb_stap!=-1,scaf_linkedList._virtual_helix, domain_idx ,bs_low=list[0],bs_high=list[idx-1])
        scaf_linkedList.append(domain)
        domain+=1
        appendDomain(list[idx:],now_stap,scaf_linkedList,0,domain_idx)
    else:
        appendDomain(list,hyb_stap,scaf_linkedList,idx+1,domain_idx)

if __name__ == '__main__':
    scaf_linkedList = LinkedList(0)
    list = [[0,0,0,0,1],[1,0,0,0,1],[2,0,0,0,2]]
    hyb_stap = list[0][4]
    appendDomain(list, hyb_stap,scaf_linkedList,0,0)

    try:
        print(a)
    except:
        print 'an error'

