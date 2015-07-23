__author__ = 'jie'
from strandrep.toehold_item_controller import ToeholdItemController
from cadnano.gui.views.pathview import pathstyles as styles
from PyQt5.QtCore import QRectF, Qt, QPointF, QEvent
from PyQt5.QtGui import QBrush, QPen, QFont, QColor, QPainterPath
from PyQt5.QtWidgets  import QGraphicsPathItem, QGraphicsRectItem
from cadnano.gui.views.pathview.strand.endpointitem import EndpointItem

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

#TODO: create different toehold paint paths for toehold going in different directions
_PATH_START = QPointF(_HBW, _HBW)

# insert path up high idx
_INSERT_PATH_UP_HIGH_IDX = QPainterPath()
_PATH_UP_HIGH_STOP = QPointF(-_BW, -.5*_BW)
_ARC_RECT = QRectF(-.6*_BW,-.5*_BW,1*_BW,1*_BW)
_insertGen(_INSERT_PATH_UP_HIGH_IDX, _PATH_START+QPointF(-0.7*_BW,0),_ARC_RECT, _PATH_UP_HIGH_STOP,-90,180)
_INSERT_PATH_UP_HIGH_IDX.translate(_OFFSET1, 0)
_INSERT_PATH_UP_HIGH_RECT = _INSERT_PATH_UP_HIGH_IDX.boundingRect()

# insert path up low index
_INSERT_PATH_UP_LOW_IDX = QPainterPath()
_PATH_UP_LOW_STOP = QPointF(_BW,-.5*_BW)
_ARC_RECT = QRectF(-.4*_BW,-.5*_BW,1*_BW,1*_BW)
_insertGen(_INSERT_PATH_UP_LOW_IDX,_PATH_START+QPointF(.7*_BW,0),_ARC_RECT,_PATH_UP_LOW_STOP,-90,-180)
_INSERT_PATH_UP_LOW_IDX.translate(_OFFSET1,0)
_INSERT_PATH_UP_LOW_RECT = _INSERT_PATH_UP_LOW_IDX.boundingRect()

# insert path down high index
_INSERT_PATH_DOWN_HIGH_IDX = QPainterPath()
_PATH_DOWN_HIGH_STOP = QPointF(-_BW, 1.5*_BW)
_ARC_RECT = QRectF(-.6*_BW, .5*_BW,1*_BW,1*_BW)
_insertGen(_INSERT_PATH_DOWN_HIGH_IDX, _PATH_START+QPointF(-0.7*_BW,0),_ARC_RECT, _PATH_DOWN_HIGH_STOP,90,-180)
_INSERT_PATH_DOWN_HIGH_IDX.translate(_OFFSET1, 0)
_INSERT_PATH_DOWN_HIGH_RECT = _INSERT_PATH_DOWN_HIGH_IDX.boundingRect()

# insert path down low index
_INSERT_PATH_DOWN_LOW_IDX = QPainterPath()
_PATH_DOWN_LOW_STOP = QPointF(_BW,1.5*_BW)
_ARC_RECT = QRectF(-.4*_BW, .5*_BW,1*_BW,1*_BW)
_insertGen(_INSERT_PATH_DOWN_LOW_IDX,_PATH_START+QPointF(.7*_BW,0),_ARC_RECT,_PATH_DOWN_LOW_STOP,90,180)
_INSERT_PATH_DOWN_LOW_IDX.translate(_OFFSET1,0)
_INSERT_PATH_DOWN_LOW_RECT = _INSERT_PATH_DOWN_LOW_IDX.boundingRect()

# insert path down low index



# _BIG_RECT = _DEFAULT_RECT.united(_INSERT_PATH_UP_HIGH_RECT)
# _BIG_RECT = _BIG_RECT.united(_INSERT_PATH_DOWNRect)
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
    def __init__(self,toeholdList,virtual_helix_item,prime):
        super(ToeholdItem, self).__init__(virtual_helix_item)
        self._virtual_helix_item = virtual_helix_item
        self._toehold_list = toeholdList
        self._domain = toeholdList._domain
        self._prime = prime
        self.hide()
        _insert_path = InsertionPath()
        self._is_on_top = is_on_top = self._virtual_helix_item.isStrandOnTop(self._domain)
        self._is_high_idx = self._toehold_list._is_high_idx
        y = 0 if is_on_top else _BW
        if self._is_high_idx:
            self.setPos(_BW*self._domain._high_idx, y)
        else:
            self.setPos(_BW*self._domain._low_idx, y)
        self.setZValue(styles.ZINSERTHANDLE)
        self.setPen(QPen(QColor(self._domain.oligo().color()), styles.PATH_STRAND_STROKE_WIDTH))
        self.setBrush(QBrush(Qt.NoBrush))
        path = _insert_path.getInsert(is_on_top,self._is_high_idx)
        self.setPath(path)
        self.show()
        self._toehold_item_controller = ToeholdItemController(self)

    def deleteItem(self,domain):
        # hide item from view
        self.hide()