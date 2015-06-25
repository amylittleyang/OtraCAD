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
        # read staple segments and xovers
        for i in range(len(stap)):
                five_vh, five_idx, three_vh, three_idx = stap[i]
                if five_vh == -1 and three_vh == -1:
                    continue  # null base
                if isSegmentStartOrEnd(StrandType.STAPLE, vh_num, i, five_vh,\
                                       five_idx, three_vh, three_idx):
                    stap_seg[vh_num].append(i)
                if five_vh != vh_num and three_vh != vh_num:  # special case
                    stap_seg[vh_num].append(i)  # end segment on a double crossover
                if is3primeXover(StrandType.STAPLE, vh_num, i, three_vh, three_idx):
                    stap_xo[vh_num].append((i, three_vh, three_idx))
            assert (len(stap_seg[vh_num]) % 2 == 0)
        # install staple segments -> modify to incorporate scaffold xover?
       for i in range(0, len(stap_seg[vh_num]), 2):
                low_idx = stap_seg[vh_num][i]
                high_idx = stap_seg[vh_num][i + 1]
                ## low_idx and high_idx should be coordinates; need hybridized domain on scaf as last parameter
                stap_domain = Domain(helix,i/2,bs_low=stap[low_idx],bs_high=stap[high_idx])
                stap_strand_LinkedList.append(stap_domain)

    for i in range(len(scaf)):
                five_vh, five_idx, three_vh, three_idx = scaf[i]
                if five_vh == -1 and three_vh == -1:
                    scaf[i].append(-1)
                    scaf_update.append(scaf[i])
                    continue  # null base
                elif hybridized(stap[i]):
                    stapNum = getStapleIdx(i,stap_seg,vh_num)
                    scaf[i].append(stapNum)
                else:
                    scaf[i].append(-1)

                scaf_update.append(scaf[i])
                #print 'list appended'

                if isSegmentStartOrEnd(StrandType.SCAFFOLD, vh_num, i, five_vh,\
                                       five_idx, three_vh, three_idx):
                    scaf_seg[vh_num].append(i)
                if five_vh != vh_num and three_vh != vh_num:  # special case
                    scaf_seg[vh_num].append(i)  # end segment on a double crossover
                if is3primeXover(StrandType.SCAFFOLD, vh_num, i, three_vh, three_idx):
                    scaf_xo[vh_num].append((i, three_vh, three_idx))
        # install scaffold segments
      for i in range(0, len(scaf_seg[vh_num]), 2):
        low_idx = scaf_seg[vh_num][i]
        high_idx = scaf_seg[vh_num][i + 1]
        populateLinkedList(low_idx,high_idx,scaf_update,helix,scaf_strand_LinkedList)


# calls recursive function
def populateLinkedList(low_idx,high_idx,scaf_update,vh,scaf_linkedList):
    list = []
    print 'low idx = '+ str(low_idx) + ', high idx = '+ str(high_idx)
    for i in range(low_idx,high_idx+1):
        print 'i = '+ str(i)
        list.append(scaf_update[i])
    hyb_stap = list[0][4]
    appendDomain(list, hyb_stap,scaf_linkedList,0)



# recursion, needs testing
def appendDomain(list,hyb_stap,scaf_linkedList,idx):
    if idx == len(list) or len(list) == 0:
        domain = Domain(scaf_linkedList._virtual_helix, scaf_linkedList._length ,bs_low=list[0],bs_high=list[len(list)-1],hyb_strand=hyb_stap)
        scaf_linkedList.append(domain)
        return
    now_stap = list[idx][4]
    if now_stap != hyb_stap:
        domain = Domain(scaf_linkedList._virtual_helix, scaf_linkedList._length ,bs_low=list[0],bs_high=list[idx-1],hyb_strand=hyb_stap)
        scaf_linkedList.append(domain)
        appendDomain(list[idx:],now_stap,scaf_linkedList,0)
    else:
        appendDomain(list,hyb_stap,scaf_linkedList,idx+1)

def hybridized(list):
    for i in range(len(list)):
        list[i] = list[i]+1
    return any(list)


def getStapleIdx(idx,stap_seg,vh_num):
    for i in range(0,len(stap_seg[vh_num]),2):
        l = stap_seg[vh_num][i]
        h = stap_seg[vh_num][i+1]
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