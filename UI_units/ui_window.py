__author__ = 'jie'
from PyQt5 import uic
from cadnano.gui.views.pathview.tools.pathtoolmanager import PathToolManager
from cadnano.gui.views.pathview.pathrootitem import PathRootItem
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QGraphicsItem
from cadnano.gui.views.customqgraphicsview import CustomQGraphicsView
from PyQt5.QtWidgets import QDockWidget
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5 import Qt
class MainWindow(QMainWindow):



    #somewhere in constructor:
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui_window.ui', self)
        self.setupUI()

    def setupUI(self):
        root = QFileInfo(__file__).absolutePath()
        self.actionOpen.setIcon(QIcon(root+'/images/Live Mail.ico'))
        self.actionSave.setIcon(QIcon(root+'/images/489751-Floppy_Disk-128.png'))
        self.actionSelect.setIcon(QIcon(root+'/images/mouse.png'))
        self.actionRip_off.setIcon(QIcon(root+'/images/rip_off.png'))
        self.setWindowTitle('AnimDNA')
        self.actionCreate_toehold.setIcon(QIcon(root+'/images/transformation.png'))
        self.setWindowIcon((QIcon(root+'/images/bug.png')))
        self.main_splitter = QtWidgets.QSplitter(self.centralwidget)
        self.path_splitter = QtWidgets.QSplitter(self.main_splitter)
        self.renderView = CustomQGraphicsView(self.path_splitter)

        #TODO: set min renderView width & dock width(to display complete tool box)
        dock = QDockWidget('An Example')
        dock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetClosable)
        self.dockWidget = dock
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,self.dockWidget)
        # show after user wants new transformation
        self.dockWidget.hide()

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
#         self.path_tool_manager = PathToolManager(self,self.path_toolbar)
    #end def




