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
from cadnano.gui.views.customqgraphicsview import CustomQGraphicsView
from PyQt5.QtCore import QObject, pyqtSignal
from cadnano.cnproxy import ProxyObject,ProxySignal

class MainWindow(QMainWindow):

    #somewhere in constructor:
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui_window.ui', self)
        self.setupUI()

    def setupUI(self):
        root = QFileInfo(__file__).absolutePath()
        #self.newAct = QAction(QIcon(root + '/images/new.png'), "&New", self,
        #        shortcut=QKeySequence.New, statusTip="Create a new file",
        #        triggered=self.newFile)
        self.actionOpen.setIcon(QIcon(root+'/images/Live Mail.ico'))
        self.actionSave.setIcon(QIcon(root+'/images/489751-Floppy_Disk-128.png'))
        from PyQt5 import QtCore, QtGui, QtWidgets
        self.main_splitter = QtWidgets.QSplitter(self.centralwidget)
        self.path_splitter = QtWidgets.QSplitter(self.main_splitter)
        self.renderView = CustomQGraphicsView(self.path_splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.renderView.sizePolicy().hasHeightForWidth())
        self.renderView.setSizePolicy(sizePolicy)
        self.renderView.setMinimumSize(QtCore.QSize(0, 0))
        self.renderView.setMouseTracking(True)
        self.renderView.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.renderView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.renderView.setLineWidth(0)
        self.renderView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.renderView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.renderView.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing|QtGui.QPainter.TextAntialiasing)
        self.renderView.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.renderView.setObjectName("renderView")
        self.renderView.setupGL(self)
        self.gridLayout.addWidget(self.main_splitter, 0, 0, 1, 1)
#        MainWindow.setCentralWidget(self.centralwidget)
        self.action_modify = QtWidgets.QAction(self)
        self.action_modify.setCheckable(True)

    def updateRenderView(self,doc_ctrl):
         doc = doc_ctrl._document
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
         self.path_tool_manager = PathToolManager(self,self.path_toolbar)
    #end def




