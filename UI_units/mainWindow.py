__author__ = 'jie'
import os
from PyQt5 import uic
from cadnano25.cadnano.gui.views.pathview.pathrootitem import PathRootItem
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGraphicsScene,QVBoxLayout
from PyQt5.QtWidgets import QMainWindow,QAction
from PyQt5.QtWidgets import QGraphicsItem
from cadnano25.cadnano.gui.views.customqgraphicsview import CustomQGraphicsView
from PyQt5 import QtWidgets,QtCore,QtGui
from UI_units.toolbar import ToolBar
from UI_units.dockWidget import DockWidget
from UI_units.menu_bar import MenuBar
class MainWindow(QMainWindow):



    def __init__(self):
        super(MainWindow, self).__init__()
        # read .ui file from QtDesigner
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        f = open(os.path.join(__location__, 'ui_window.ui'));
        uic.loadUi(f, self)
        self.doc = None
        self.setupUI()

    def setupUI(self):
        # actions
        root = QFileInfo(__file__).absolutePath()
        # self.actionUndo = QAction(QIcon(root+'/images/Undo-icon.png'),"undo",self)
        # self.actionMerge_domain = QAction(self)
        # self.actionCreate_toehold = QAction(self)
        # self.actionResize_toehold = QAction(self)
        # self.actionRemove_toehold = QAction(self)

        # connect menuBar, toolBar, dockWidget to self(mainWindow)
        self.dockWidget = DockWidget(self)
        self.menuBar = MenuBar(self)
        self.toolBar = ToolBar(self)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,self.dockWidget)


        # main window setup
        root = QFileInfo(__file__).absolutePath()
        self.setWindowTitle('OtraCAD')
        self.setWindowIcon((QIcon(root+'/images/bug.png')))
        # splitter allows user control the size of child widgets by dragging the boundary between the children
        self.main_splitter = QtWidgets.QSplitter(self.centralwidget)
        self.path_splitter = QtWidgets.QSplitter(self.main_splitter)
        # renderView is where .json file is rendered in the window;
        # CustomQGraphicsView extends QGraphicsView, allow zooming in/out and drag by using "command+click"
        self.renderView = CustomQGraphicsView(self.path_splitter)




        # size polices
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



    def updateRenderView(self,doc_ctrl):
        # set up render view to render imported .json file
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

    def setDoc(self,doc):
        # set documents for all child widgets
        self.doc = doc
        self.dockWidget.doc = doc
        self.toolBar.doc = doc


