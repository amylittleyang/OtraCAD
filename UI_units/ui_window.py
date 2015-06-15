__author__ = 'jie'
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
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

