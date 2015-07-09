__author__ = 'jie'
from PyQt5.QtGui import QIcon
from cadnano.document import Document
from fileio import domain_decode
import io
from cadnano.gui.controllers.documentcontroller import DocumentController
from PyQt5.QtWidgets import QToolBar,QMessageBox,QFileDialog
from PyQt5.QtCore import QFileInfo
import json

class ToolBar(QToolBar):
    def __init__(self,mainWindow):
        super(ToolBar, self).__init__(None)
        self.mainWindow = mainWindow
        self.doc = mainWindow.doc
        self.actionOpen = mainWindow.actionOpen
        self.actionSave = mainWindow.actionSave
        self.actionCreate_toehold = mainWindow.actionCreate_toehold
        self.setupUI()

    def setupUI(self):
        root = QFileInfo(__file__).absolutePath()
        self.actionOpen.setIcon(QIcon(root+'/images/Live Mail.ico'))
        self.actionOpen.triggered.connect(self.actionOpenTriggeredSlot)
        self.actionSave.setIcon(QIcon(root+'/images/489751-Floppy_Disk-128.png'))
        self.actionSave.triggered.connect(self.actionSaveTriggeredSlot)
        self.actionCreate_toehold.setIcon(QIcon(root+'/images/transformation.png'))
        self.actionCreate_toehold.triggered.connect(self.mainWindow.dockWidget.actionCreate_toeholdTriggeredSlot)

    def actionOpenTriggeredSlot(self):
        file_dialog = QFileDialog()
# the name filters must be a list
        file_dialog.setNameFilters(["Jason files (*.json)", "All files (*)"])
        file_dialog.selectNameFilter("Jason files (*.json)")
# show the dialog
        boo = file_dialog.exec_()
        myFile = None
        if(boo):
            selectedFiles = file_dialog.selectedFiles()
            myFile = selectedFiles[0]
        if(myFile is not None):
            #call cadnano json parsing funcality here and pass jasonFile. Check to see if result is correct
            messageBox = QMessageBox()
            messageBox.setText(myFile +' selected')
            messageBox.exec_()
            path = myFile

            with io.open(path, 'r', encoding='utf-8') as fd:
                dict = json.load(fd)
                doc = Document()
                doc.mainWindow = self.mainWindow
                doc.dc = DocumentController(doc)
                domain_decode.decode(doc,dict)
                self.mainWindow.setDoc(doc)

            messageBox = QMessageBox()
            messageBox.setText('parsed')
            messageBox.exec_()
        else:
            messageBox = QMessageBox()
            messageBox.setText('No file selected')
            messageBox.exec_()




    def actionSaveTriggeredSlot(self):
        pass