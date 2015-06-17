__author__ = 'jie'
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from cadnano import app

from cadnano.gui.views.pathview.pathtoolbar import PathToolBar
from cadnano.gui.views.pathview.parttoolbar import PartToolBar
from cadnano.gui.views.pathview.colorpanel import ColorPanel

from cadnano.gui.views.pathview.tools.pathtoolmanager import PathToolManager
from cadnano.gui.views.sliceview.slicerootitem import SliceRootItem
from cadnano.gui.views.pathview.pathrootitem import PathRootItem

from cadnano.gui.views.sliceview.tools.slicetoolmanager import SliceToolManager
import cadnano.gui.ui.mainwindow.ui_mainwindow as ui_mainwindow
import cadnano.util
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtCore import QFileInfo, QSettings
from PyQt5.QtCore import QPoint, QSize
from cadnano.cnproxy import DummySignal
from PyQt5.QtGui import QPaintEngine, QIcon
from PyQt5.QtWidgets import QGraphicsObject, QGraphicsScene
from PyQt5.QtWidgets import QGraphicsView, QMainWindow
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem
from PyQt5.QtWidgets import QApplication, QWidget, QAction
from PyQt5.QtWidgets import QSizePolicy, QFrame

from PyQt5.QtCore import QObject, pyqtSignal
from cadnano.cnproxy import ProxyObject,ProxySignal

class MainWindow(QMainWindow):

    #somewhere in constructor:
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('initialization/ui_window.ui', self)
        self.setupUI()

    def setupUI(self):
        root = QFileInfo(__file__).absolutePath()
        #self.newAct = QAction(QIcon(root + '/images/new.png'), "&New", self,
        #        shortcut=QKeySequence.New, statusTip="Create a new file",
        #        triggered=self.newFile)
        self.actionOpen.setIcon(QIcon(root+'/images/Live Mail.ico'))
        self.actionSave.setIcon(QIcon(root+'/images/489751-Floppy_Disk-128.png'))

    def updateRenderView(self,doc_ctrl):
         self.pathscene = QGraphicsScene(parent=self.renderView)
         self.pathroot = PathRootItem(rect=self.pathscene.sceneRect(),\
                                     parent=None,\
                                     window=self,\
                                     document= doc_ctrl._document)
         self.pathroot.setFlag(QGraphicsItem.ItemHasNoContents)
         self.pathscene.addItem(self.pathroot)
         self.pathscene.setItemIndexMethod(QGraphicsScene.NoIndex)
         assert self.pathroot.scene() == self.pathscene
         self.renderView.setScene(self.pathscene)
         self.renderView.scene_root_item = self.pathroot
         self.renderView._scale_fit_factor = 0.9
         self.renderView._name = 'renderView'
    #end def




