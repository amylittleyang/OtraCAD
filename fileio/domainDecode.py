__author__ = 'jie'
# -*- coding: utf-8 -*-

import json
import io
from collections import defaultdict
from cadnano.document import Document
from cadnano.enum import LatticeType, StrandType
from cadnano.color import Color
import cadnano.preferences as prefs
from cadnano import setBatch, getReopen, setReopen
from cadnano.part.refresholigoscmd import RefreshOligosCommand
from strandrep.domain import Domain

def decodeFile(filename, document=None):
    with io.open(filename, 'r', encoding='utf-8') as fd:
        nno_dict = json.load(fd)
    if document is None:
        document = Document()
    decode(document, nno_dict)
    return document

def decode(document,obj):
    num_bases = len(obj['vstrands'][0]['scaf'])
    if num_bases % 32 == 0:
        lattice_type = LatticeType.SQUARE
    elif num_bases % 21 == 0:
        lattice_type = LatticeType.HONEYCOMB
    else:
        raise IOError("error decoding number of bases")


    # DETERMINE MAX ROW,COL
    max_row_json = max_col_json = 0
    for helix in obj['vstrands']:
        max_row_json = max(max_row_json, int(helix['row'])+1)
        max_col_json = max(max_col_json, int(helix['col'])+1)

    # CREATE PART ACCORDING TO LATTICE TYPE
    if lattice_type == LatticeType.HONEYCOMB:
        steps = num_bases // 21
        # num_rows = max(30, max_row_json, cadnano.app().prefs.honeycombRows)
        # num_cols = max(32, max_col_json, cadnano.app().prefs.honeycombCols)
        num_rows = max(30, max_row_json, prefs.HONEYCOMB_PART_MAXROWS)
        num_cols = max(32, max_col_json, prefs.HONEYCOMB_PART_MAXCOLS)
        part = document.addHoneycombPart(num_rows, num_cols, steps)
    elif lattice_type == LatticeType.SQUARE:
        is_SQ_100 = True  # check for custom SQ100 format
        for helix in obj['vstrands']:
            if helix['col'] != 0:
                is_SQ_100 = False
                break
        if is_SQ_100:
            # num_rows, num_cols = 100, 1
            num_rows, num_cols = 40, 30
        else:
            num_rows, num_cols = 40, 30
        steps = num_bases // 32
        # num_rows = max(30, max_row_json, cadnano.app().prefs.squareRows)
        # num_cols = max(32, max_col_json, cadnano.app().prefs.squareCols)
        num_rows = max(30, max_row_json, prefs.SQUARE_PART_MAXROWS)
        num_cols = max(32, max_col_json, prefs.SQUARE_PART_MAXCOLS)
        part = document.addSquarePart(num_rows, num_cols, steps)
        # part = SquarePart(document=document, max_row=num_rows, max_col=num_cols, max_steps=steps)
    else:
        raise TypeError("Lattice type not recognized")
    # document._addPart(part, use_undostack=False)
    setBatch(True)
    # POPULATE VIRTUAL HELICES
    ordered_coord_list = []
    vh_num_to_coord = {}
    for helix in obj['vstrands']:
        vh_num = helix['num']
        row = helix['row']
        col = helix['col']
        scaf= helix['scaf']
        coord = (row, col)
        vh_num_to_coord[vh_num] = coord
        ordered_coord_list.append(coord)
    # make sure we retain the original order
    for vh_num in sorted(vh_num_to_coord.keys()):
        row, col = vh_num_to_coord[vh_num]
        part.createVirtualHelix(row, col, use_undostack=False)
    if not getReopen():
        setBatch(False)
    part.setImportedVHelixOrder(ordered_coord_list)
    setReopen(False)
    setBatch(False)

    num_helices = len(obj['vstrands']) - 1
    scaf_seg = defaultdict(list)
    scaf_xo = defaultdict(list)
    stap_seg = defaultdict(list)
    stap_xo = defaultdict(list)

    for helix in obj['vstrands']:
        vh_num = helix['num']
        row = helix['row']
        col = helix['col']
        scaf = helix['scaf']
        stap = helix['stap']
        insertions = helix['loop']
        skips = helix['skip']
        vh = part.virtualHelixAtCoord((row, col))
        scaf_strand_LinkedList = vh._scaf_LinkedList
        stap_strand_LinkedList = vh._scaf_LinkedList
        scaf_update = []
        stap_update = []

        # read scaf segments and xovers

        for i in range(len(scaf)):
            five_vh, five_idx, three_vh, three_idx = scaf[i]
            if five_vh == -1 and three_vh == -1:
                continue  # null base
            if isSegmentStartOrEnd(StrandType.SCAFFOLD, vh_num, i, five_vh,\
                                       five_idx, three_vh, three_idx):
                scaf_seg[vh_num].append(i)
            if five_vh != vh_num and three_vh != vh_num:  # special case
                scaf_seg[vh_num].append(i)  # end segment on a double crossover
            if is3primeXover(StrandType.SCAFFOLD, vh_num, i, three_vh, three_idx):
                scaf_xo[vh_num].append((i, three_vh, three_idx))
            # read staple segments and xovers; update stap .json
        for i in range(len(stap)):
                five_vh, five_idx, three_vh, three_idx = stap[i]
                if five_vh == -1 and three_vh == -1:
                    stap[i].append(-1)
                    stap_update.append(stap[i])
                    continue  # null base
                elif hybridized(scaf[i]):
                    scafNum = getStrandIdx(i,scaf_seg,vh_num)
                    stap[i].append(scafNum)
                stap_update.append(stap[i])

                if isSegmentStartOrEnd(StrandType.STAPLE, vh_num, i, five_vh,\
                                       five_idx, three_vh, three_idx):
                    stap_seg[vh_num].append(i)
                if five_vh != vh_num and three_vh != vh_num:  # special case
                    stap_seg[vh_num].append(i)  # end segment on a double crossover
                if is3primeXover(StrandType.STAPLE, vh_num, i, three_vh, three_idx):
                    stap_xo[vh_num].append((i, three_vh, three_idx))

        assert (len(stap_seg[vh_num]) % 2 == 0)
        # update scaf .json
        for i in range(len(scaf)):
                five_vh, five_idx, three_vh, three_idx = scaf[i]
                if five_vh == -1 and three_vh == -1:
                    scaf[i].append(-1)
                    scaf_update.append(scaf[i])
                    continue  # null base
                elif hybridized(stap[i]):
                    stapNum = getStrandIdx(i,stap_seg,vh_num)
                    scaf[i].append(stapNum)
                    scaf_update.append(scaf[i])
            # install scaffold segments
        for i in range(0, len(scaf_seg[vh_num]), 2):
            low_idx = scaf_seg[vh_num][i]
            high_idx = scaf_seg[vh_num][i + 1]
            installLinkedList(low_idx,high_idx,scaf_update,scaf_strand_LinkedList)


        # install staple segments -> modify to incorporate scaffold xover?
        for i in range(0, len(stap_seg[vh_num]), 2):
            low_idx = stap_seg[vh_num][i]
            high_idx = stap_seg[vh_num][i + 1]
            installLinkedList(low_idx,high_idx,stap_update,stap_strand_LinkedList)
            ## low_idx and high_idx should be coordinates; need hybridized domain on scaf as last parameter


# calls recursive function
def installLinkedList(low_idx,high_idx,strand_update,strand_linkedList):
    list = []
#    print 'low idx = '+ str(low_idx) + ', high idx = '+ str(high_idx)
    for i in range(low_idx,high_idx+1):
#        print 'i = '+ str(i)
        list.append(strand_update[i])
    hyb_strand = list[0][4]
    appendDomain(list, hyb_strand,strand_linkedList,0)

# recursion, tested
def appendDomain(list,hyb_stap,strand_linkedList,idx):
    if idx == len(list) or len(list) == 0:
        domain = Domain(strand_linkedList._virtual_helix, strand_linkedList._length ,bs_low=list[0],bs_high=list[len(list)-1],hyb_strand=hyb_stap)
        strand_linkedList.append(domain)
        return
    now_stap = list[idx][4]
    if now_stap != hyb_stap:
        print(strand_linkedList._length)
        domain = Domain(strand_linkedList._virtual_helix, strand_linkedList._length ,bs_low=list[0],bs_high=list[idx-1],hyb_strand=hyb_stap)
        strand_linkedList.append(domain)
        appendDomain(list[idx:],now_stap,strand_linkedList,0)
    else:
        appendDomain(list,hyb_stap,strand_linkedList,idx+1)


def hybridized(list):
    list_copy = []
    for i in range(len(list)):
        list_copy.append(list[i]+1)
    return any(list)


def getStrandIdx(idx,strand_seg,vh_num):
    for i in range(0,len(strand_seg[vh_num]),2):
        l = strand_seg[vh_num][i]
        h = strand_seg[vh_num][i+1]
        if l <= idx and idx <= h:
            return i/2

def isSegmentStartOrEnd(strandtype, vh_num, base_idx, five_vh, five_idx, three_vh, three_idx):
    """Returns True if the base is a breakpoint or crossover."""
    if strandtype == StrandType.SCAFFOLD:
        offset = 1
    else:
        offset = -1
    if (five_vh == vh_num and three_vh != vh_num):
        return True
    if (five_vh != vh_num and three_vh == vh_num):
        return True
    if (vh_num % 2 == 0 and five_vh == vh_num and five_idx != base_idx-offset):
        return True
    if (vh_num % 2 == 0 and three_vh == vh_num and three_idx != base_idx+offset):
        return True
    if (vh_num % 2 == 1 and five_vh == vh_num and five_idx != base_idx+offset):
        return True
    if (vh_num % 2 == 1 and three_vh == vh_num and three_idx != base_idx-offset):
        return True
    if (five_vh == -1 and three_vh != -1):
        return True
    if (five_vh != -1 and three_vh == -1):
        return True
    return False

def is3primeXover(strandtype, vh_num, base_idx, three_vh, three_idx):
    """Returns True of the three_vh doesn't match vh_num, or three_idx
    is not a natural neighbor of base_idx."""
    if three_vh == -1:
        return False
    if vh_num != three_vh:
        return True
    if strandtype == StrandType.SCAFFOLD:
        offset = 1
    else:
        offset = -1
    if (vh_num % 2 == 0 and three_vh == vh_num and three_idx != base_idx+offset):
        return True
    if (vh_num % 2 == 1 and three_vh == vh_num and three_idx != base_idx-offset):
        return True










if __name__ == '__main__':
    from strandrep.domain import Domain
    from strandrep.linked_list import LinkedList
    from cadnano.enum import StrandType
    from collections import defaultdict

    vh_num = 2
    helix = 2
    stap_seg = defaultdict(list)
    scaf_seg = defaultdict(list)
    stap_xo = defaultdict(list)
    scaf_xo = defaultdict(list)
    scaf_update = []
    stap_update = []
    stap_strand_LinkedList = LinkedList(StrandType.STAPLE,2)
    scaf_strand_LinkedList = LinkedList(StrandType.SCAFFOLD,2)

    scaf = [[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[3,83,2,84],[2,83,2,85],[2,84,2,86],[2,85,2,87],[2,86,2,88],[2,87,2,89],[2,88,2,90],[2,89,2,91],[2,90,2,92],[2,91,2,93],[2,92,2,94],[2,93,2,95],[2,94,2,96],[2,95,2,97],[2,96,2,98],[2,97,2,99],[2,98,2,100],[2,99,2,101],[2,100,2,102],[2,101,2,103],[2,102,2,104],[2,103,2,105],[2,104,2,106],[2,105,2,107],[2,106,2,108],[2,107,2,109],[2,108,2,110],[2,109,2,111],[2,110,2,112],[2,111,2,113],[2,112,2,114],[2,113,2,115],[2,114,2,116],[2,115,2,117],[2,116,2,118],[2,117,2,119],[2,118,2,120],[2,119,2,121],[2,120,2,122],[2,121,2,123],[2,122,2,124],[2,123,2,125],[2,124,2,126],[2,125,2,127],[2,126,2,128],[2,127,2,129],[2,128,2,130],[2,129,1,130],[1,131,2,132],[2,131,2,133],[2,132,2,134],[2,133,2,135],[2,134,2,136],[2,135,2,137],[2,136,2,138],[2,137,2,139],[2,138,2,140],[2,139,2,141],[2,140,2,142],[2,141,2,143],[2,142,2,144],[2,143,2,145],[2,144,2,146],[2,145,2,147],[2,146,2,148],[2,147,2,149],[2,148,2,150],[2,149,2,151],[2,150,2,152],[2,151,2,153],[2,152,2,154],[2,153,2,155],[2,154,2,156],[2,155,2,157],[2,156,2,158],[2,157,2,159],[2,158,2,160],[2,159,2,161],[2,160,2,162],[2,161,2,163],[2,162,2,164],[2,163,2,165],[2,164,2,166],[2,165,2,167],[2,166,2,168],[2,167,2,169],[2,168,2,170],[2,169,2,171],[2,170,2,172],[2,171,2,173],[2,172,2,174],[2,173,2,175],[2,174,2,176],[2,175,2,177],[2,176,2,178],[2,177,3,178],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
    stap = [[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[2,84,-1,-1],[2,85,2,83],[2,86,2,84],[2,87,2,85],[2,88,2,86],[2,89,2,87],[2,90,2,88],[2,91,2,89],[2,92,2,90],[2,93,2,91],[2,94,2,92],[2,95,2,93],[2,96,2,94],[2,97,2,95],[2,98,2,96],[2,99,2,97],[2,100,2,98],[2,101,2,99],[2,102,2,100],[2,103,2,101],[2,104,2,102],[2,105,2,103],[2,106,2,104],[2,107,2,105],[2,108,2,106],[2,109,2,107],[2,110,2,108],[2,111,2,109],[2,112,2,110],[2,113,2,111],[2,114,2,112],[2,115,2,113],[2,116,2,114],[-1,-1,2,115],[2,118,-1,-1],[2,119,2,117],[3,119,2,118],[2,121,3,120],[2,122,2,120],[2,123,2,121],[2,124,2,122],[2,125,2,123],[2,126,2,124],[2,127,2,125],[2,128,2,126],[2,129,2,127],[2,130,2,128],[2,131,2,129],[2,132,2,130],[2,133,2,131],[2,134,2,132],[2,135,2,133],[2,136,2,134],[2,137,2,135],[2,138,2,136],[2,139,2,137],[2,140,2,138],[2,141,2,139],[2,142,2,140],[2,143,2,141],[2,144,2,142],[2,145,2,143],[2,146,2,144],[2,147,2,145],[2,148,2,146],[-1,-1,2,147],[2,150,-1,-1],[2,151,2,149],[3,151,2,150],[2,153,3,152],[2,154,2,152],[2,155,2,153],[2,156,2,154],[2,157,2,155],[2,158,2,156],[2,159,2,157],[2,160,2,158],[2,161,2,159],[2,162,2,160],[2,163,2,161],[2,164,2,162],[2,165,2,163],[2,166,2,164],[2,167,2,165],[2,168,2,166],[2,169,2,167],[2,170,2,168],[2,171,2,169],[2,172,2,170],[2,173,2,171],[2,174,2,172],[2,175,2,173],[2,176,2,174],[2,177,2,175],[2,178,2,176],[-1,-1,2,177],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]

    for i in range(len(scaf)):
        five_vh, five_idx, three_vh, three_idx = scaf[i]
        if five_vh == -1 and three_vh == -1:
            continue  # null base
        if isSegmentStartOrEnd(StrandType.SCAFFOLD, vh_num, i, five_vh,\
                                       five_idx, three_vh, three_idx):
            scaf_seg[vh_num].append(i)
        if five_vh != vh_num and three_vh != vh_num:  # special case
            scaf_seg[vh_num].append(i)  # end segment on a double crossover
        if is3primeXover(StrandType.SCAFFOLD, vh_num, i, three_vh, three_idx):
            scaf_xo[vh_num].append((i, three_vh, three_idx))
        # read staple segments and xovers; update stap .json
    for i in range(len(stap)):
                five_vh, five_idx, three_vh, three_idx = stap[i]
                if five_vh == -1 and three_vh == -1:
                    stap[i].append(-1)
                    stap_update.append(stap[i])
                    continue  # null base
                elif hybridized(scaf[i]):
                    scafNum = getStrandIdx(i,scaf_seg,vh_num)
                    stap[i].append(scafNum)
                stap_update.append(stap[i])

                if isSegmentStartOrEnd(StrandType.STAPLE, vh_num, i, five_vh,\
                                       five_idx, three_vh, three_idx):
                    stap_seg[vh_num].append(i)
                if five_vh != vh_num and three_vh != vh_num:  # special case
                    stap_seg[vh_num].append(i)  # end segment on a double crossover
                if is3primeXover(StrandType.STAPLE, vh_num, i, three_vh, three_idx):
                    stap_xo[vh_num].append((i, three_vh, three_idx))

    assert (len(stap_seg[vh_num]) % 2 == 0)
        # update scaf .json
    for i in range(len(scaf)):
                five_vh, five_idx, three_vh, three_idx = scaf[i]
                if five_vh == -1 and three_vh == -1:
                    scaf[i].append(-1)
                    scaf_update.append(scaf[i])
                    continue  # null base
                elif hybridized(stap[i]):
                    stapNum = getStrandIdx(i,stap_seg,vh_num)
                    scaf[i].append(stapNum)
                    scaf_update.append(scaf[i])
            # install scaffold segments
    for i in range(0, len(scaf_seg[vh_num]), 2):
            low_idx = scaf_seg[vh_num][i]
            high_idx = scaf_seg[vh_num][i + 1]
            installLinkedList(low_idx,high_idx,scaf_update,scaf_strand_LinkedList)


        # install staple segments -> modify to incorporate scaffold xover?
    for i in range(0, len(stap_seg[vh_num]), 2):
            low_idx = stap_seg[vh_num][i]
            high_idx = stap_seg[vh_num][i + 1]
            installLinkedList(low_idx,high_idx,stap_update,stap_strand_LinkedList)
            ## low_idx and high_idx should be coordinates; need hybridized domain on scaf as last parameter

    print('stap domains')
    curr = stap_strand_LinkedList._head
    while True:
        print 'domain idx %d low base %d, high base %d, hybridized to scaffold domain %d, on helix number %d' % (curr._idx,curr._bs_low[1],curr._bs_high[3],curr._hyb_strand,curr._vhNum)
        print curr._bs_high
        curr = curr._next
        if curr == None:
            break

    print 'scaf domains'
    curr = scaf_strand_LinkedList._head
    while True:
        print 'domain idx %d low base %d, high base %d, hybridized to staple %d, on helix number %d' % (curr._idx,curr._bs_low[1],curr._bs_high[3],curr._hyb_strand,curr._vhNum)
        curr = curr._next
        if curr == None:
            break