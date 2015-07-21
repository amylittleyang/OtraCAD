__author__ = 'jie'
from PyQt5.QtGui import QIcon
from cadnano.document import Document
from fileio import domain_decode
import io
from cadnano.gui.controllers.documentcontroller import DocumentController
from PyQt5.QtWidgets import QToolBar,QMessageBox,QFileDialog,QAction
from PyQt5.QtCore import QFileInfo
import json

class ToolBar(QToolBar):
    def __init__(self,mainWindow):
        super(ToolBar, self).__init__(None)
        # get actions from main window
        self.mainWindow = mainWindow
        self.doc = mainWindow.doc
        # get actions from mainWindow parsed from .ui file
        self.actionOpen = mainWindow.actionOpen
        self.actionSave = mainWindow.actionSave
        self.actionCreate_toehold = mainWindow.actionCreate_toehold
        self.setupUI() # and connect action to slot

    def setupUI(self):
        # set icon for actions
        root = QFileInfo(__file__).absolutePath()
        self.actionOpen.setIcon(QIcon(root+'/images/Live Mail.ico'))
        self.actionOpen.triggered.connect(self.actionOpenTriggeredSlot)
        self.actionSave.setIcon(QIcon(root+'/images/489751-Floppy_Disk-128.png'))
        self.actionSave.triggered.connect(self.actionSaveTriggeredSlot)
        self.actionCreate_toehold.setIcon(QIcon(root+'/images/transformation.png'))
        self.actionCreate_toehold.triggered.connect(self.mainWindow.dockWidget.actionCreate_toeholdTriggeredSlot)


    def actionOpenTriggeredSlot(self):
        # user wants to import a .json file
        file_dialog = QFileDialog()
        file_dialog.setNameFilters(["Jason files (*.json)", "All files (*)"])
        file_dialog.selectNameFilter("Jason files (*.json)")
        # show file dialog
        boo = file_dialog.exec_()
        myFile = None
        # if file dialog is executed
        if(boo):
            selectedFiles = file_dialog.selectedFiles()
            # get the first and only file selected
            myFile = selectedFiles[0]
        if(myFile is not None):
            messageBox = QMessageBox()
            # show file path
            messageBox.setText(myFile +' selected')
            messageBox.exec_()
            path = myFile

            # use python function to read .json file
            with io.open(path, 'r', encoding='utf-8') as fd:
                dict = json.load(fd)
                doc = Document()
                doc.mainWindow = self.mainWindow
                doc.dc = DocumentController(doc)
                # re-construct strand & oligo, render them on renderView
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