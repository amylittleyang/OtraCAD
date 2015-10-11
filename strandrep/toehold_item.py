__author__ = 'jie'
from strandrep.toehold_item_controller import ToeholdItemController
from cadnano.gui.views.pathview import pathstyles as styles
from PyQt5.QtCore import QRectF, Qt, QPointF, QEvent
from PyQt5.QtGui import QBrush, QPen, QFont, QColor, QPainterPath
from PyQt5.QtWidgets  import QGraphicsPathItem, QGraphicsRectItem
from math import floor

_BASE_WIDTH = _BW = styles.PATH_BASE_WIDTH
_HALF_BASE_WIDTH = _HBW = _BASE_WIDTH / 2
_OFFSET1 = _BASE_WIDTH / 4
_DEFAULT_RECT = QRectF(0, 0, _BW, _BW)
_B_PEN = QPen(styles.BLUE_STROKE, styles.INSERTWIDTH)
_R_PEN = QPen(styles.RED_STROKE, styles.SKIPWIDTH)
_NO_PEN = QPen(Qt.NoPen)

def _insertGen(path,start,rect,stop,deg1,deg2):
    path.moveTo(start)
    path.arcTo(rect,deg1,deg2)
    path.lineTo(stop)
# end def
_PATH_START = QPointF(_HBW, _HBW)

# insert path up high idx
_INSERT_PATH_UP_HIGH_IDX = QPainterPath()
_PATH_UP_HIGH_STOP = QPointF(-.65*_BW, -.5*_BW)
_ARC_RECT = QRectF(-.6*_BW,-.5*_BW,1*_BW,1*_BW)
_insertGen(_INSERT_PATH_UP_HIGH_IDX, _PATH_START+QPointF(-0.7*_BW,0),_ARC_RECT, _PATH_UP_HIGH_STOP,-90,180)
_INSERT_PATH_UP_HIGH_IDX.translate(_OFFSET1, 0)
_INSERT_PATH_UP_HIGH_RECT = _INSERT_PATH_UP_HIGH_IDX.boundingRect()
#_BIG_RECT = _DEFAULT_RECT.united(_DEFAULT_RECT,_INSERT_PATH_UP_HIGH_RECT)


# insert path up low index
_INSERT_PATH_UP_LOW_IDX = QPainterPath()
_PATH_UP_LOW_STOP = QPointF(.9*_BW,-.5*_BW)
_ARC_RECT = QRectF(-.4*_BW,-.5*_BW,1*_BW,1*_BW)
_insertGen(_INSERT_PATH_UP_LOW_IDX,_PATH_START+QPointF(0.2*_BW,0),_ARC_RECT,_PATH_UP_LOW_STOP,-90,-180)
_INSERT_PATH_UP_LOW_IDX.translate(_OFFSET1,0)
_INSERT_PATH_UP_LOW_RECT = _INSERT_PATH_UP_LOW_IDX.boundingRect()
#_BIG_RECT = _DEFAULT_RECT.united(_DEFAULT_RECT,_INSERT_PATH_UP_LOW_RECT)


# insert path down high index
_INSERT_PATH_DOWN_HIGH_IDX = QPainterPath()
_PATH_DOWN_HIGH_STOP = QPointF(-1.1*_BW, 1.5*_BW)
_ARC_RECT = QRectF(-.6*_BW, .5*_BW,1*_BW,1*_BW)
_insertGen(_INSERT_PATH_DOWN_HIGH_IDX, _PATH_START+QPointF(-0.65*_BW,0),_ARC_RECT, _PATH_DOWN_HIGH_STOP,90,-180)
_INSERT_PATH_DOWN_HIGH_IDX.translate(_OFFSET1, 0)
_INSERT_PATH_DOWN_HIGH_RECT = _INSERT_PATH_DOWN_HIGH_IDX.boundingRect()
#_BIG_RECT = _DEFAULT_RECT.united(_DEFAULT_RECT,_INSERT_PATH_DOWN_HIGH_RECT)


# insert path down low index
_INSERT_PATH_DOWN_LOW_IDX = QPainterPath()
_PATH_DOWN_LOW_STOP = QPointF(.75*_BW,1.5*_BW)
_ARC_RECT = QRectF(-.4*_BW, .5*_BW,1*_BW,1*_BW)
_insertGen(_INSERT_PATH_DOWN_LOW_IDX,_PATH_START+QPointF(.25*_BW,0),_ARC_RECT,_PATH_DOWN_LOW_STOP,90,180)
_INSERT_PATH_DOWN_LOW_IDX.translate(_OFFSET1,0)
_INSERT_PATH_DOWN_LOW_RECT = _INSERT_PATH_DOWN_LOW_IDX.boundingRect()
#_BIG_RECT = _DEFAULT_RECT.united(_DEFAULT_RECT,_INSERT_PATH_DOWN_LOW_RECT)


# insert path down low index



#_BIG_RECT = _BIG_RECT.united(_INSERT_PATH_DOWNRect)
_B_PEN2 = QPen(styles.BLUE_STROKE, 2)
_OFFSET2   = _BW*0.75
_FONT = QFont(styles.THE_FONT, 10, QFont.Bold)
# _BIG_RECT.adjust(-15, -15, 30, 30)
# Bases are drawn along and above the insert path.
# These calculations revolve around fixing the characters at a certain
# percentage of the total arclength.
# The fraction of the insert that comes before the first character and
# after the last character is the padding, and the rest is divided evenly.
_FRACTION_INSERT_TO_PAD = .10

class InsertionPath(object):
    """
    This is just the shape of the Insert item
    """

    def __init__(self):
        super(InsertionPath, self).__init__()
    # end def

    def getPen(self):
        return _B_PEN
    # end def

    def getInsert(self, is_top,is_high_idx):
        # decide which path to use
        if is_top:
            if is_high_idx:
                return _INSERT_PATH_UP_HIGH_IDX
            else:
                return _INSERT_PATH_UP_LOW_IDX
        else:
            if is_high_idx:
                return _INSERT_PATH_DOWN_HIGH_IDX
            else:
                return _INSERT_PATH_DOWN_LOW_IDX
    # end def
# end class

class ToeholdItem(QGraphicsPathItem):
    '''
    view toehold item renders a toehold on render view;
    one toehold item is created for each toehold list;
    toehold item hidden only when no toehold domain exists in toehold list
    '''
    def __init__(self,toehold,strand_item,prime):
        super(ToeholdItem, self).__init__(strand_item)
        self._toehold = toehold
        self._strand_item = strand_item
        self._virtual_helix_item = strand_item._virtual_helix_item
        self._toehold_list = toehold._toehold_list
        self._domain = toehold._toehold_list._domain
        self._prime = prime
        self.hide()
        self._insert_path = InsertionPath()
        self._is_on_top = is_on_top = self._virtual_helix_item.isStrandOnTop(self._domain)
        self._is_high_idx = self._toehold_list._is_high_idx
        y = 0 if is_on_top else _BW
        if self._is_high_idx:
            self.setPos(_BW*self._domain._high_idx, y)
        else:
            self.setPos(_BW*self._domain._low_idx, y)
        self._toehold_item_controller = ToeholdItemController(self,self._toehold_list)
        self.setZValue(styles.ZINSERTHANDLE)
        self.updateColor(False)
        self._click_area = QGraphicsRectItem(self)
        self.setAcceptHoverEvents(True)
        self._click_area.mousePressEvent = self.mousePressEvent
        self._click_area.hoverMoveEvent = self.hoverMoveEvent
        self._click_area.hoverLeaveEvent = self.hoverLeaveEvent

    def updateColor(self, value):
        oligo = self._domain.oligo()
        bool = oligo.shouldHighlight()
        if value == True:
            bool = not oligo.shouldHighlight()

        if bool:
            color = QColor(oligo.color())
            color.setAlpha(128)
            pen = QPen(color, styles.PATH_STRAND_HIGHLIGHT_STROKE_WIDTH)
            pen.setCosmetic(False)
            self.setPen(pen)
        else:
            color = QColor(oligo.color())
            pen = QPen(color, styles.PATH_STRAND_STROKE_WIDTH)
            pen.setCosmetic(False)
            self.setPen(pen)

        brush = self.brush()
        brush.setColor(color)
        self.setBrush(brush)
        path = self._insert_path.getInsert(self._is_on_top,self._is_high_idx)
        self.setPath(path)
        self.show()


    def deleteItem(self,domain):
        # hide item from view
        self.hide()

    def mousePressEvent(self, event):
        domain = self._domain
        doc = domain._doc
        t = self._toehold_list
        doc.setActiveDomain(domain)
        if event.modifiers() & Qt.ShiftModifier:
            selection = doc.selectedToehold()
            if t in selection:
                doc.removeSelectedToehold(t)
            else:
                doc.addSelectedToehold(t)
        else:
            #uncolor all previously added domain, clear from selection
            doc.removeAllToeholdFromSelection()
            doc.removeAllDomainFromSelection()
            doc.setActiveOligo(domain.oligo())


    def setSelectedColor(self, value):
        if value == True:
            color = QColor("#ff3333")
            pen_width = styles.PATH_STRAND_HIGHLIGHT_STROKE_WIDTH
        else:
            oligo = self._domain.oligo()
            color = QColor(oligo.color())
            pen_width = styles.PATH_STRAND_STROKE_WIDTH
            if oligo.shouldHighlight():
                color.setAlpha(128)
        pen = QPen(color,pen_width)
        self.setPen(pen)

    def toeholdRemovedFromSelectionSlot(self,t):
        self.setSelectedColor(False)
        if self._is_high_idx:
            self._strand_item.toeholdCapHigh().setSelectedColor(False)
        else:
            self._strand_item.toeholdCapLow().setSelectedColor(False)

    def toeholdSelectedSlot(self,t):
        self.setSelectedColor(True)
        if self._is_high_idx:
            self._strand_item.toeholdCapHigh().setSelectedColor(True)
        else:
            self._strand_item.toeholdCapLow().setSelectedColor(True)


    def hoverMoveEvent(self, event):
        """
        Parses a mouseMoveEvent to extract strandSet and base index,
        forwarding them to approproate tool method as necessary.
        """

        td = self.toeholdDomainToStr()
        self._strand_item.partItem().updateStatusBar("Toehold domains at %s: %s " % (self._domain._name, td))


    def hoverLeaveEvent(self, event):
        self._strand_item.partItem().updateStatusBar("")

    def toeholdDomainToStr(self):
        str = ""
        for d in self._toehold_list._toehold_list:
            str = str + d._name + " "
        return str

    def destroy(self):
        scene = self.scene()
        scene.removeItem(self._click_area)
        self._click_area = None
        scene.removeItem(self)








