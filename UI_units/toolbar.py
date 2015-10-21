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
        self.actionMerge_domain = mainWindow.actionMerge_domain
        self.actionCreate_toehold = mainWindow.actionCreate_toehold
        self.actionResize_toehold = mainWindow.actionResize_toehold
        self.actionRemove_toehold = mainWindow.actionRemove_toehold
        self.actionRip_off = mainWindow.actionRip_off

        self.setupUI() # and connect action to slot

    def setupUI(self):
        # set icon for actions
        root = QFileInfo(__file__).absolutePath()

        self.actionMerge_domain.setIcon(QIcon(root+'/images/merge.png'))
        self.actionMerge_domain.triggered.connect(self.actionMerge_domainTriggeredSlot)

        self.actionOpen.setIcon(QIcon(root+'/images/Live Mail.ico'))
        self.actionOpen.triggered.connect(self.actionOpenTriggeredSlot)

        self.actionRip_off.setIcon(QIcon(root+'/images/rip_off.png'))
        self.actionRip_off.triggered.connect(self.mainWindow.dockWidget.actionRipOffTriggeredSlot)

        self.actionRemove_toehold.setIcon(QIcon(root+'/images/remove_toehold.png'))
        self.actionRemove_toehold.triggered.connect(self.actionRemoveToeholdTriggeredSlot)


        self.actionSave.setIcon(QIcon(root+'/images/489751-Floppy_Disk-128.png'))
        self.actionSave.triggered.connect(self.actionSaveTriggeredSlot)

        self.actionCreate_toehold.setIcon(QIcon(root+'/images/transformation.png'))
        self.actionCreate_toehold.triggered.connect(self.mainWindow.dockWidget.actionCreate_toeholdTriggeredSlot)

        self.actionResize_toehold.setIcon(QIcon(root+'/images/resize_toehold.png'))
        self.actionResize_toehold.triggered.connect(self.mainWindow.dockWidget.actionResizeToeholdTriggeredSlot)

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

    def actionRemoveToeholdTriggeredSlot(self):
        if self.doc is None:
            msg = QMessageBox()
            msg.setText("No doc.")
            msg.exec_()
            return
        t_list = self.doc._selected_toehold
        #print(t_list.__len__())
        if t_list.__len__() is not 1:
            msg = QMessageBox()
            msg.setText("Must select one toehold")
            msg.exec_()
            return
        else:
            toehold = t_list[0]._toehold_list[0]
            toehold._domain.removeToehold(toehold)

    def actionMerge_domainTriggeredSlot(self):
        if self.doc is None:
            msg = QMessageBox()
            msg.setText("No files imported.")
            msg.exec_()
            return
        d_list = self.doc._selected_domain
        if len(d_list) is not 2:
            msg = QMessageBox()
            msg.setText("Select two domains.")
            msg.exec_()
            return
        # doc is not None, only two domains selected
        one = d_list[0]
        print(one._name)
        two = d_list[1]
        one.merge_with(two)
        self.doc._selected_domain = []

