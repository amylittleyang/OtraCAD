__author__ = 'jie'
import string
from operator import attrgetter
from strandrep.create_toehold_command import CreateToeholdCommand
from strandrep.remove_toehold_command import RemoveToeholdCommand
import cadnano.util as util
from cadnano.cnproxy import ProxyObject, ProxySignal



class Domain(ProxyObject):
    def __init__(self,strandset,low_idx,high_idx,bs_low = None, bs_high = None, hyb_strand=None):
        super(Domain, self).__init__(strandset)
        self._doc = strandset.document()
        self._hyb_strand_idx = hyb_strand
        self._index = strandset.length()
        self._vh = strandset._virtual_helix
        self._vhNum = self._vh._number
        self._type = strandset._strand_type
        # domain naming
        if self._type == 0:
            self._type_str = 'scaf'
            self._name = string.ascii_lowercase[self._index]+str(self._vhNum)
        elif self._type == 1:
            self._type_str ='stap'
            self._name = string.ascii_lowercase[self._index]+str(self._vhNum)+'*'
        else:
            self._type = 'overhang'
            self._name = 'T'+ str(self._vhNum)+str(self._index)     # fix naming
        self._sequence = None
        #coordinates and indexes
        self._bs_low  = bs_low
        self._bs_high = bs_high
        self._strandset = strandset
        self._low_idx = low_idx
        self._high_idx = high_idx
        self._length = high_idx-low_idx+1
        # domain3p and domain5p refer to previous and proceeding node in scaf/stap linked list
        self._domain_3p = None
        self._domain_5p = None
        # connection3p and connection5p refer to xover to different domains
        self._connection_5p = None
        self._connection_3p = None
        self._is_5p_connection_xover = None
        self._is_3p_connection_xover = None
        self._hyb_domain = None
        self._unhyb_domain = 0;
        # orientation on virtual helix
        self._is_drawn_5_to_3 = self._strandset.isDrawn5to3()
        if  self._is_drawn_5_to_3:
            self.idx5Prime = self.lowIdx
            self.idx3Prime = self.highIdx
            self.connectionLow = self.connection5p
            self.connectionHigh = self.connection3p
            self.setConnectionLow = self.setConnection5p
            self.setConnectionHigh = self.setConnection3p
            self.setIsConnectionHighXover = self.setIs3pConnectionXover
            self.setIsConnectionLowXover = self.setIs5pConnectionXover
            self.isConnectionHighXover = self.is3pConnectionXover
            self.isConnectionLowXover = self.is5pConnectionXover
        else:
            self.idx5Prime = self.highIdx
            self.idx3Prime = self.lowIdx
            self.connectionLow = self.connection3p
            self.connectionHigh = self.connection5p
            self.setConnectionLow = self.setConnection3p
            self.setConnectionHigh = self.setConnection5p
            self.setIsConnectionHighXover = self.setIs5pConnectionXover
            self.setIsConnectionLowXover = self.setIs3pConnectionXover
            self.isConnectionHighXover = self.is5pConnectionXover
            self.isConnectionLowXover = self.is3pConnectionXover

        if self._hyb_strand_idx > 0:
            self._loop = False
        else:
            self._loop = True

        # properties used for creating toehold
        self._toehold_list_3p = None
        self._toehold_list_5p = None
        self._last_toehold_cmd = None
        # refers to the 5' or 3' domain actually operated on in creating toehold
        self._endDomain = None

 ### Singals
    togglePreviewRipOffSignal = ProxySignal(name="togglePreviewRipOffSignal") #previewRipOffSlot in strand item, toggle hide/show of strand item
    toeholdremovedSignal = ProxySignal(object,object,name='toeholdRemovedSignal') # toeholdRemovedSlot in strand item
    toeholdAddedSignal = ProxySignal(object,object,name = 'toeholdAddedSignal')   # toeholdAddedSlot in strand item
    strandHasNewOligoSignal = ProxySignal(ProxyObject, name='strandHasNewOligoSignal') # hasNewOligoSlot in abstract strand item
    strandUpdateSignal = ProxySignal(ProxyObject, name='strandUpdateSignal') #pyqtSignal(QObject)
    strandRemovedSignal = ProxySignal(ProxyObject, name='strandRemovedSignal') #pyqtSignal(QObject)  # strand
    strandSelectedSignal = ProxySignal(ProxyObject,name='strandSelectedSignal')
    strandRemovedFromSelectionSignal = ProxySignal(ProxyObject,name='strandRemovedFromSelectionSignal')
    def strandFilter(self):
        return self._strandset.strandFilter()

    def setName(self,scaf_index):
        if scaf_index == -1:
            self._name = str(self._vhNum) + "M" + str(self._unhyb_domain)
            self._unhyb_domain += 1
        else:
            try:
                self._name = string.ascii_lowercase[scaf_index] + str(self._vhNum) + "*"
            except:
                print("self_idx = %d, vh = %d" %(self.lowIdx(),self._vhNum))


    def name(self):
        return self._name

    def oligo(self):
        return self._oligo

    def isStaple(self):
        return self._strandset._strand_type == 1

    def generator5pStrand(self):
        node0 = node = self
        f = attrgetter('_connection_5p')
        # while node and originalCount == 0:
        #     yield node  # equivalent to: node = node._strand5p
        #     node = f(node)
        #     if node0 == self:
        #         originalCount += 1
        while node:
            yield node  # equivalent to: node = node._strand5p
            node = f(node)
            if node0 == node:
                break


    def generator3pStrand(self):
        # return a generator of all strand linked in the 3' direction
        node0 = node = self
        f = attrgetter('_connection_3p')
        while node:
            yield node  # equivalent to: node = node._strand5p
            node = f(node)
            if node0 == node:
                break

    def connection3p(self):
        return self._connection_3p

    def connection5p(self):
        return self._connection_5p

    def idxs(self):
        return (self._low_idx, self._high_idx)

    def lowIdx(self):
        return self._low_idx
    # end def

    def highIdx(self):
        return self._high_idx
    # end def

    def strandSet(self):
        return self._strandset

    def setConnection3p(self, strand):
        self._connection_3p = strand
    # end def

    def setConnection5p(self, strand):
        self._connection_5p = strand
    # end def
    def length(self):
        return self._length

    def virtualHelix(self):
        return self._vh

    def oligo(self):
        return self._oligo

    def document(self):
        return self._doc


    def setDomain5p(self,domain):
        self._domain_5p = domain

    def setDomain3p(self,domain):
        self._domain_3p = domain

    def setToehold3p(self,toeholdList):
        self._toehold_list_3p = toeholdList

    def setToehold5p(self,toeholdList):
        self._toehold_list_5p = toeholdList

    def toeholdList3p(self):
        return self._toehold_list_3p

    def toeholdList5p(self):
        return self._toehold_list_5p


    def setOligo(self, new_oligo, emit_signal=True):
        self._oligo = new_oligo
        if emit_signal:
            self.strandHasNewOligoSignal.emit(self)

    def totalLength(self):
        """
        includes the length of insertions in addition to the bases
        """
        tL = 0
        insertions = self.insertionsOnStrand()

        for insertion in insertions:
            tL += insertion.length()
        return tL + self.length()

    def insertionsOnStrand(self, idxL=None, idxH=None):
        """
        if passed indices it will use those as a bounds
        """
        insertions = []
        coord = self.virtualHelix().coord()
        insertionsDict = self.part().insertions()[coord]
        sortedIndices = sorted(insertionsDict.keys())
        if idxL == None:
            idxL, idxH = self.idxs()
        for index in sortedIndices:
            insertion = insertionsDict[index]
            if idxL <= insertion.idx() <= idxH:
                insertions.append(insertion)
            # end if
        # end for
        return insertions

    def part(self):
        return self._strandset.part()

    def sequence(self, for_export=False):
        seq = self._sequence
        if seq:
            return util.markwhite(seq) if for_export else seq
        elif for_export:
            return ''.join(['?' for x in range(self.totalLength())])
        return ''
    # end def
    def isScaffold(self):
        return self._strandset.isScaffold()

    def is5pConnectionXover(self):
        if self._is_5p_connection_xover is not None:
            return self._is_5p_connection_xover
        else:
            return False

    def is3pConnectionXover(self):
        if self._is_3p_connection_xover is not None:
            return self._is_3p_connection_xover
        else:
            return False

    def setIs5pConnectionXover(self,bool):
        self._is_5p_connection_xover = bool

    def setIs3pConnectionXover(self,bool):
        self._is_3p_connection_xover = bool

    def toehold3p(self):
        return self._toehold_list_3p

    def toehold5p(self):
        return self._toehold_list_5p

    def toeholdChanged(self,prime,checked=True):
        # called by dock widget to delete/add toehold
        '''
        doesn't create/delete toehold on self;
        instead, get corresponding end domain on oligo and apply operation on end domain;
        '''
        if prime == 3:
            endDomain = self._oligo._domain3p
        else:
            endDomain = self._oligo._domain5p
        self._endDomain = endDomain
        # get dict for state of toehold commands
        dict = self._oligo._toehold_cmd_dict
        cmd = CreateToeholdCommand(self._vh,endDomain,prime)
        if checked: #create new toehold at a prime
            cmd.redo()
            dict[prime] = cmd
        else: # remove a toehold at a prime
            cmd.undo()
            dict[prime] = None

    def createToehold(self,toehold,use_undostack = True):
        # put removed toeholds back, no need to check if_can_create_toehold
        cmd = CreateToeholdCommand(self._vh,toehold._domain,toehold._prime)
        list = [cmd]
        d = "createToehold %s at %s".format(toehold._name,toehold._domain._name)
        util.execCommandList(self,list,d,use_undostack=use_undostack)

    def hasToehold(self):
        return (self.toehold3p() is not None) or (self.toehold5p() is not None)

    def toeholds(self):
        t = []
        if self.toehold3p():
            t.append(self.toehold3p())
        if self.toehold5p():
            t.append(self.toehold5p())
        return t

    def canCreateToeholdAt(self,prime):
        '''
        return true if endDomain has no connection to other domains at prime and no
        toehold has already been created at prime
        '''
        if self._oligo._is_loop:
                return False
        # get endDomain reference for oligo
        if prime == 3:
            curr = curr0 = self
            while curr._connection_3p is not None:
                curr = curr._connection_3p
                if curr == curr0:
                    break
            self._oligo._domain3p = curr
            return (curr.connection3p() is None) and (curr.toehold3p() is None)
        elif prime == 5:
            curr = curr0 = self
            while curr._connection_5p is not None:
                curr = curr._connection_5p
                if curr == curr0:
                    break
            self._oligo._domain5p = curr
            return (curr.connection5p() is None) and (curr.toehold5p() is None)

    def toeholdChangeAccepted(self):
        # triggered when user accepts a toehold operation
        dict = self._oligo._toehold_cmd_dict
        stack = []
        '''
        reset all toehold command state to None in oligo command dict;
        undo all executed command, command will be redo-ed after pushed onto undo stack;
        '''
        for prime,cmd in dict.iteritems():
            if cmd is not None:
                stack.append(cmd)
                cmd.undo()
                dict[prime] = None
        d = '%s create toehold' % self._name
        # record the accepted sequence of command as a macro
        util.execCommandList(self,stack,d,use_undostack=True)


    def toeholdChangeRejected(self):
        # undo all executed command
        if self._endDomain is None:
            return
        dict = self._oligo._toehold_cmd_dict
        for prime,cmd in dict.iteritems():
            if cmd is not None:
                cmd.undo()
                dict[prime] = None

    def removeToehold(self,toehold,use_undostack=True):
        cmd = RemoveToeholdCommand(self,toehold)
        stack=[cmd]
        d = '%s remove toehold' % self._name
        util.execCommandList(self,stack,d,use_undostack=use_undostack)

    def undoStack(self):
        return self._strandset.undoStack()

    def merge_with(self,domain):
        '''
        method to merge self with another domain;
        Need to: adjust index; rm second domain; rm tick mark (emit signal to notify strand_item
        after model is changed); inherit connections, toeholds,domain3p/5p from second domain;
        '''
        # adjust indices & domain_3p/5p reference
        if self._low_idx > domain._low_idx:
            self._low_idx = domain._low_idx
            if self._is_drawn_5_to_3:
                self._domain_5p = domain._domain_5p
                if self._domain_5p:
                    self._domain_5p._domain_3p = self
            else:
                self._domain_3p = domain._domain_3p
                if self._domain_3p:
                    self._domain_3p._domain_5p = self
        else:
            self._high_idx = domain._high_idx
            if self._is_drawn_5_to_3:
                self._domain_3p = domain._domain_3p
                if self._domain_3p:
                    self._domain_3p._domain_5p = self
            else:
                self._domain_5p = domain._domain_5p
                if self._domain_5p:
                    self._domain_5p._domain_3p = self
        # length
        self._length = self.length() + domain.length()
        # domain name
        self._name = self._name+"_"+ domain._name
        # toehold and connection
        if domain.connection3p() and domain.connection3p() != self:
            self.setConnection3p(domain.connection3p())
            self.setIs3pConnectionXover(domain.is3pConnectionXover())
        if domain.connection5p() and domain.connection5p() != self:
            self.setConnection5p(domain.connection5p())
            self.setIs5pConnectionXover(domain.is5pConnectionXover())
        if not domain.connection3p():
            self.setConnection3p(None)
        if not domain.connection5p():
            self.setConnection5p(None)
        if domain.toehold3p():
            self.setToehold3p(domain.toehold3p())
        if domain.toehold5p():
            self.setToehold5p(domain.toehold5p())

        #destroy second strand, refresh oligo
        domain.strandRemovedSignal.emit(domain)
        self.strandUpdateSignal.emit(self)



