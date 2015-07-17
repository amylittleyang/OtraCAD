__author__ = 'jie'
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFileInfo
class MenuBar(QMenuBar):
    def __init__(self,mainWindow):
        self._main_window = mainWindow
        self.actionRedo = mainWindow.actionRedo
        self.actionUndo = mainWindow.actionUndo
        self.setupUI()

    def setupUI(self):
        root = QFileInfo(__file__).absolutePath()
        self.actionUndo.setIcon(QIcon(root+'/images/Undo-icon.png'))
        self.actionRedo.setIcon(QIcon(root+'/images/Redo-icon.png'))
