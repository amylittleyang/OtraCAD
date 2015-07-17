__author__ = 'jie'
from PyQt5.QtWidgets import QGraphicsLineItem
from strandrep.toehold_item_controller import ToeholdItemController
from cadnano.gui.views.pathview import pathstyles as styles
from PyQt5.QtCore import QRectF, Qt, QPointF, QEvent

from PyQt5.QtGui import QBrush, QPen, QFont, QColor, QPainterPath
from PyQt5.QtGui import QTransform, QTextCursor
from PyQt5.QtWidgets  import QGraphicsPathItem, QGraphicsRectItem
from PyQt5.QtWidgets  import QGraphicsTextItem

_BASE_WIDTH = _BW = styles.PATH_BASE_WIDTH
_HALF_BASE_WIDTH = _HBW = _BASE_WIDTH / 2
_OFFSET1 = _BASE_WIDTH / 4
_DEFAULT_RECT = QRectF(0, 0, _BW, _BW)
_B_PEN = QPen(styles.BLUE_STROKE, styles.INSERTWIDTH)
_R_PEN = QPen(styles.RED_STROKE, styles.SKIPWIDTH)
_NO_PEN = QPen(Qt.NoPen)

def _insertGen(path,start, c1, p1, stop):
    path.moveTo(start)
    path.lineTo(start + QPointF(0.1*_BW,0))
    path.quadTo(c1, p1)
    path.lineTo(stop)
# end def


_PATH_START = QPointF(_HBW, _HBW)
_PATH_DOWN_C1 = QPointF(1 *_BW, 1.5 *_BW)
_PATH_DOWN_P1 = QPointF(2 * _BW, 1.6 *_BW)
_PATH_DOWN_STOP = QPointF(3*_BW, 1.6 *_BW)

_PATH_UP_C1 = QPointF(1 *_BW, -1 *_BW)
_PATH_UP_P1 = QPointF(2 * _BW, -1.1 *_BW)
_PATH_UP_STOP = QPointF(3*_BW, -1.1 *_BW)

_INSERT_PATH_UP = QPainterPath()
_insertGen(_INSERT_PATH_UP, _PATH_START, _PATH_UP_C1, _PATH_UP_P1, _PATH_UP_STOP)
_INSERT_PATH_UP.translate(_OFFSET1, 0)
_INSERT_PATH_UP_RECT = _INSERT_PATH_UP.boundingRect()
_INSERT_PATH_DOWN = QPainterPath()

_insertGen(_INSERT_PATH_DOWN, _PATH_START, _PATH_DOWN_C1, _PATH_DOWN_P1,_PATH_DOWN_STOP)

_INSERT_PATH_DOWN.translate(_OFFSET1, 0)
_INSERT_PATH_DOWNRect = _INSERT_PATH_DOWN.boundingRect()


_BIG_RECT = _DEFAULT_RECT.united(_INSERT_PATH_UP_RECT)
_BIG_RECT = _BIG_RECT.united(_INSERT_PATH_DOWNRect)
_B_PEN2 = QPen(styles.BLUE_STROKE, 2)
_OFFSET2   = _BW*0.75
_FONT = QFont(styles.THE_FONT, 10, QFont.Bold)
_BIG_RECT.adjust(-15, -15, 30, 30)
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

    def getInsert(self, is_top):
        if is_top:
            return _INSERT_PATH_UP
        else:
            return _INSERT_PATH_DOWN
    # end def
# end class

class ToeholdItem(QGraphicsPathItem):
    def __init__(self,domain,virtual_helix_item,prime):
        super(ToeholdItem, self).__init__(virtual_helix_item)
        self._virtual_helix_item = virtual_helix_item
        self._domain = domain
        self._prime = prime
        self.hide()
        _insert_path = InsertionPath()
        self._is_on_top = is_on_top = self._virtual_helix_item.isStrandOnTop(domain)
        y = 0 if is_on_top else _BW
        if ((not domain._is_drawn_5_to_3) and (self._prime == 5)) or\
                (domain._is_drawn_5_to_3 and (self._prime == 3)):
            self.setPos(_BW*self._domain._high_idx, y)
        else:
            self.setPos(_BW*self._domain._low_idx, y)
        self.setZValue(styles.ZINSERTHANDLE)
        self.setPen(QPen(QColor(domain.oligo().color()), styles.PATH_STRAND_STROKE_WIDTH))
        self.setBrush(QBrush(Qt.NoBrush))
        self.setPath(_insert_path.getInsert(is_on_top))
        self.show()
        self._toehold_item_controller = ToeholdItemController(self)

    def deleteItem(self,domain):
        self.hide()