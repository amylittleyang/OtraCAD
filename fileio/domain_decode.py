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
        stap_strand_LinkedList = vh._stap_LinkedList

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
                '''
                append a fifth element to coordinate list; if staple is hybridized to a scaffold
                domain at the location, get the index of the scaffold domain on scaffold
                strandset and append it; if not hybridized to any scaffold domain, append -1.
                '''
                if five_vh == -1 and three_vh == -1:
                    stap[i].append(-1) # null base, cannot hybridize to any domain
                    continue  # null base
                elif hybridized(scaf[i]): # true if hybridized to scaffold at the position
                    scafNum = getStrandIdx(i,scaf_seg,vh_num=vh_num) # get hybridized scaffold domain index
                    stap[i].append(scafNum)

                if isSegmentStartOrEnd(StrandType.STAPLE, vh_num, i, five_vh,\
                                       five_idx, three_vh, three_idx):
                    stap_seg[vh_num].append(i)
                if five_vh != vh_num and three_vh != vh_num:  # special case
                    stap_seg[vh_num].append(i)  # end segment on a double crossover
                if is3primeXover(StrandType.STAPLE, vh_num, i, three_vh, three_idx):
                    stap_xo[vh_num].append((i, three_vh, three_idx))

        assert (len(stap_seg[vh_num]) % 2 == 0)
        # update scaf .json, append hybridized strand index to coordinate
        for i in range(len(scaf)):
                five_vh, five_idx, three_vh, three_idx = scaf[i]
                if five_vh == -1 and three_vh == -1:
                    scaf[i].append(-1)
                    continue  # null base
                elif hybridized(stap[i]):
                    stapNum = getStrandIdx(i,stap_seg,vh_num=vh_num)
                    scaf[i].append(stapNum)

        new_scaf_seg = []
        # install scaffold segments
        for i in range(0, len(scaf_seg[vh_num]), 2):
            low_idx = scaf_seg[vh_num][i]
            high_idx = scaf_seg[vh_num][i + 1]
            # split scaffold domain based on staple domain hybridized to
            installLinkedList(low_idx,high_idx,scaf,scaf_strand_LinkedList,new_scaf_seg)

        new_stap_seg = []
        #install staple segments
        for i in range(0, len(stap_seg[vh_num]), 2):
            low_idx = stap_seg[vh_num][i]
            high_idx = stap_seg[vh_num][i + 1]
            # split staple domain based on scaffold domain hybridized to
            installLinkedList(low_idx,high_idx,stap,stap_strand_LinkedList,new_stap_seg)

        # rename staple based on complement domain on scaffold
        curr0 = curr = vh._stap_LinkedList._head
        while curr:
            stap_idx = curr._low_idx
            scaf_domain_idx = getStrandIdx(stap_idx,new_scaf_seg)
            curr.setName(scaf_domain_idx)
            curr = curr._domain_3p


      # INSTALL XOVERS
    for helix in obj['vstrands']:
        vh_num = helix['num']
        row = helix['row']
        col = helix['col']
        from_vh = part.virtualHelixAtCoord((row, col))
        scaf_strand_set = from_vh.scaffoldStrandSet()
        stap_strand_set = from_vh.stapleStrandSet()
        # install scaffold xovers
        for (idx5p, to_vh_num, idx3p) in scaf_xo[vh_num]:
            strand5p = scaf_strand_set.getStrand(idx5p)
            to_vh = part.virtualHelixAtCoord(vh_num_to_coord[to_vh_num])
            strand3p = to_vh.scaffoldStrandSet().getStrand(idx3p)
            assert strand5p._vhNum == from_vh._number and strand3p._vhNum == to_vh_num
            part.createXover(strand5p, idx5p, strand3p, idx3p,
                 update_oligo=False, use_undostack=False)

        for (idx5p, to_vh_num, idx3p) in stap_xo[vh_num]:
            strand5p = stap_strand_set.getStrand(idx5p)
            to_vh = part.virtualHelixAtCoord(vh_num_to_coord[to_vh_num])
            strand3p = to_vh.stapleStrandSet().getStrand(idx3p)

            part.createXover(strand5p, idx5p, strand3p, idx3p,
                update_oligo=False, use_undostack=False)

    # connect domains into oligos; domains linked by xovers will be on the same oligo
    RefreshOligosCommand(part, include_scaffold=True,
        colors=(prefs.DEFAULT_SCAF_COLOR, prefs.DEFAULT_STAP_COLOR)).redo()

   #SET DEFAULT COLOR
    for oligo in part.oligos():
        if oligo.isStaple():
            default_color = prefs.DEFAULT_STAP_COLOR
        else:
            default_color = prefs.DEFAULT_SCAF_COLOR
        oligo.applyColor(default_color, use_undostack=False)

 #   COLORS, INSERTIONS, SKIPS
    for helix in obj['vstrands']:
        vh_num = helix['num']
        row = helix['row']
        col = helix['col']
        scaf = helix['scaf']
        stap = helix['stap']
        insertions = helix['loop']
        skips = helix['skip']
        vh = part.virtualHelixAtCoord((row, col))
        scaf_strand_set = vh.scaffoldStrandSet()
        stap_strand_set = vh.stapleStrandSet()
        # install insertions and skips
    #     for base_idx in range(len(stap)):
    #         sum_of_insert_skip = insertions[base_idx] + skips[base_idx]
    #         if sum_of_insert_skip != 0:
    #             strand = scaf_strand_set.getStrand(base_idx)
    #             strand.addInsertion(base_idx, sum_of_insert_skip, use_undostack=False)
    #     # end for
    #     # populate colors
        for base_idx, color_number in helix['stap_colors']:
            color = Color(  (color_number >> 16) & 0xFF,
                            (color_number >> 8) & 0xFF,
                            color_number & 0xFF).name()
            strand = stap_strand_set.getStrand(base_idx)
            strand.oligo().applyColor(color, use_undostack=False)
    #
    # if 'oligos' in obj:
    #     for oligo in obj['oligos']:
    #         vh_num = oligo['vh_num']
    #         idx = oligo['idx']
    #         seq = str(oligo['seq']) if oligo['seq'] is not None else ''
    #         if seq != '':
    #             coord = vh_num_to_coord[vh_num]
    #             vh = part.virtualHelixAtCoord(coord)
    #             scaf_ss = vh.scaffoldStrandSet()
    #             # stapStrandSet = vh.stapleStrandSet()
    #             strand = scaf_ss.getStrand(idx)
    #             # print "sequence", seq, vh, idx,  strand.oligo()._strand5p
    #             strand.oligo().applySequence(seq, use_undostack=False)
    # if 'modifications' in obj:
    #     # print("AD", cadnano.app().activeDocument)
    #     # win = cadnano.app().activeDocument.win
    #     # modstool = win.pathToolManager.modsTool
    #     # modstool.connectSignals(part)
    #     for mod_id, item in obj['modifications'].items():
    #         if mod_id != 'int_instances' and mod_id != 'ext_instances':
    #             part.createMod(item, mod_id)
    #     for key, mid in obj['modifications']['ext_instances'].items():
    #         strand, idx = part.getModStrandIdx(key)
    #         try:
    #             strand.addMods(mid, idx, use_undostack=False)
    #         except:
    #             print(strand, idx)
    #             raise
    #     for key in obj['modifications']['int_instances'].items():
    #         strand, idx = part.getModStrandIdx(key)
    #         try:
    #             strand.addMods(mid, idx, use_undostack=False)
    #         except:
    #             print(strand, idx)
    #             raise
        #modstool.disconnectSignals(part)
 #end def
 #
    # user not allowed to modify file after import
    document.undoStack().clear()

# calls recursive function
def installLinkedList(low_idx,high_idx,strand_update,strand_linkedList,new_strand_seg):
    '''
    get strand coordinates from low_idx to high_idx; pass all coordinates included
    to recursive function to split domain based on hybridized strand index.
    '''
    list = []
    for i in range(low_idx,high_idx+1):
        list.append(strand_update[i])
    hyb_strand = list[0][4]
    # appendDomain split strand into domains and append domains to strandset
    appendDomain(list, hyb_strand,strand_linkedList,0,low_idx,new_strand_seg)
    # put domains in strandlist after all domains are appended
    strand_linkedList.finishAppend()

# split strand into domains and append domains to strand_linkedList
def appendDomain(list,hyb_stap,strand_linkedList,idx,low,new_strand_seg):
    if idx == len(list) or len(list) == 0:
        domain = Domain(strand_linkedList,low,low+idx-1,bs_low=list[0],bs_high=list[len(list)-1])
        new_strand_seg.append(low)
        new_strand_seg.append(low+idx-1)
        strand_linkedList.append(domain)
        domain_low = strand_linkedList.domainAtIndex(-2)
        if domain_low and (not isSegmentStartOrEnd(strand_linkedList._strand_type,strand_linkedList._virtual_helix._number,low,list[0][0],list[0][1],list[0][2],list[0][3]) or len(list)==1):
            # adjacent domains on the same strand are connected by connection3p and connection5p (same as connectionLow and connectionHigh)
            domain_low.setConnectionHigh(domain)
            domain_low.setIsConnectionHighXover(True)
            domain.setConnectionLow(domain_low)
            domain.setIsConnectionLowXover(True)
        return
    now_stap = list[idx][4]
    if now_stap != hyb_stap:
        domain = Domain(strand_linkedList,low,low+idx-1,bs_low=list[0],bs_high=list[idx-1])
        new_strand_seg.append(low)
        new_strand_seg.append(low+idx-1)
        strand_linkedList.append(domain)
        domain_low = strand_linkedList.domainAtIndex(-2)
        if domain_low and not isSegmentStartOrEnd(strand_linkedList._strand_type,strand_linkedList._virtual_helix._number,low,list[0][0],list[0][1],list[0][2],list[0][3]):
            domain_low.setConnectionHigh(domain)
            domain_low.setIsConnectionHighXover(True)
            domain.setConnectionLow(domain_low)
            domain.setIsConnectionLowXover(True)
        low = low + idx
        # truncate list and pass back
        appendDomain(list[idx:],now_stap,strand_linkedList,0,low,new_strand_seg)
    else:
        appendDomain(list,hyb_stap,strand_linkedList,idx+1,low,new_strand_seg)


def hybridized(list):
    # return true if the complement strandset has strand at the query position
    list_copy = []
    for i in range(len(list)):
        print i
        list_copy.append(list[i]+1)
    return any(list)


def getStrandIdx(idx,strand_seg,vh_num = None):
    '''
    strad_seg has the start and end coordinate of all strands on all helices;
    find the strand whose start and end position bands the query index and return its index on the helix.
    '''
    if vh_num is not None:
        seg = strand_seg[vh_num]
    else:
        seg = strand_seg
    for i in range(0,len(seg),2):
        l = seg[i]
        h = seg[i+1]
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
