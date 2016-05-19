__author__ = 'jie'
from PyQt5.QtWidgets import QMenuBar, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFileInfo
class MenuBar(QMenuBar):
    '''
    menu bar at top of program;
    holds actionRedo, actionUndo;
    actions to be added: save, open, open recent;
    '''
    def __init__(self,mainWindow):
        # get actions from mainWindow
        self._main_window = mainWindow
        self.actionRedo = mainWindow.actionRedo
        self.actionUndo = mainWindow.actionUndo
        self.setupUI()

    def setupUI(self):
        # set icons for actions
        root = QFileInfo(__file__).absolutePath()
        self.actionUndo.setIcon(QIcon(root+'/images/Undo-icon.png'))
        self.actionRedo.setIcon(QIcon(root+'/images/Redo-icon.png'))
