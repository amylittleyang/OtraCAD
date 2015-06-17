# -*- coding: utf-8 -*-
__author__ = 'jie'
# controller that handles all event for all buttons in the menu bar.
from PyQt5.QtWidgets import QFileDialog   # don't understand why underscored but works fine ¬_¬
from PyQt5.QtWidgets import QMessageBox
from fileio.decode import Decoder
from document_controller import DocumentController
from cadnano.document import Document
class ToolBarController:
    def __init__(self,loader):
        self.controlledItem = loader.mainWindow.toolBar
        self.loader = loader
        self.mainWindow = loader.mainWindow

    def action_Open_Triggered_Slot(self):
        file_dialog = QFileDialog()
# the name filters must be a list
        file_dialog.setNameFilters(["Jason files (*.json)", "All files (*)"])
        file_dialog.selectNameFilter("Jason files (*.json)")
# show the dialog
        boo = file_dialog.exec_()
        if(boo):
            selectedFiles = file_dialog.selectedFiles()
            myFile = selectedFiles[0]
        if(myFile is not None):
            #call cadnano json parsing funcality here and pass jasonFile. Check to see if result is correct
            messageBox = QMessageBox()
            messageBox.setText(myFile +' selected')
            messageBox.exec_()
            path = myFile
            decoder = Decoder(toolBarController = self, path = path) # parse json file, create new document
            messageBox = QMessageBox()
            messageBox.setText('parsed')
            messageBox.exec_()


        else:
            messageBox = QMessageBox()
            messageBox.setText('No file selected')
            messageBox.exec_()

    def connect(self):
        self.loader.mainWindow.actionOpen.triggered.connect(self.action_Open_Triggered_Slot)
