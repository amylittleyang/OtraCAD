# -*- coding: utf-8 -*-
__author__ = 'jie'
# controller that handles all event for all buttons in the menu bar.
from PyQt5.QtWidgets import QFileDialog   # don't understand why underscored but works fine ¬_¬
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QCheckBox,QDialogButtonBox,QVBoxLayout,QFormLayout,QGroupBox
from fileio.decode import Decoder
from PyQt5 import Qt
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
            decoder = Decoder(toolBarController = self, path = path) # parse json file, create new document
            messageBox = QMessageBox()
            messageBox.setText('parsed')
            messageBox.exec_()
        else:
            messageBox = QMessageBox()
            messageBox.setText('No file selected')
            messageBox.exec_()
    def action_Create_toehold_Triggered_Slot(self):
        win = self.mainWindow
        dock = win.dockWidget
        dock.setWindowTitle('create toehold')
        checkBox_3p = QCheckBox('create 3-prime toehold')
        checkBox_5p = QCheckBox('create 5-prime toehold')
        buttonBox = QDialogButtonBox()
        groupBox = QGroupBox()

        layout = QFormLayout()
        layout.addWidget(checkBox_3p)
        layout.addWidget(checkBox_5p)
        layout.addWidget(buttonBox)
        groupBox.setLayout(layout)
        dock.setWidget(groupBox)
        #self.addDockWidget(Qt.RightDockWidgetArea, dock)
        # self.viewMenu.addAction(dock.toggleViewAction())
        dock.show()


    def connect(self):
        self.mainWindow.actionOpen.triggered.connect(self.action_Open_Triggered_Slot)
        self.mainWindow.actionCreate_toehold.triggered.connect(self.action_Create_toehold_Triggered_Slot)

