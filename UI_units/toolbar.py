__author__ = 'jie'
from PyQt5.QtGui import QIcon
from fileio.decode import Decoder
from PyQt5.QtWidgets import QToolBar,QMessageBox,QWidget,QFileDialog,QCheckBox,QFormLayout,QDialogButtonBox,QGroupBox,QVBoxLayout
from PyQt5.QtCore import QFileInfo

class ToolBar(QToolBar):
    def __init__(self,mainWindow):
        super(ToolBar, self).__init__(None)
        self.mainWindow = mainWindow
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
            decoder = Decoder(toolBarController = self, path = path) # parse json file, create new document
            messageBox = QMessageBox()
            messageBox.setText('parsed')
            messageBox.exec_()
        else:
            messageBox = QMessageBox()
            messageBox.setText('No file selected')
            messageBox.exec_()




    def actionSaveTriggeredSlot(self):
        pass