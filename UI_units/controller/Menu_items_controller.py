__author__ = 'jie'
# controller that handles all event for all buttons in the menu bar.
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

class MenuController:
    def __init__(self):
        pass

    def import_button_item_clicked_Slot(self):
        fileDialog = QFileDialog()
        fileDialog.show()
        fileDialog.setFileMode(QFileDialog.AnyFile)
        fileDialog.setNameFilter("json(*.json)")  #not working
        if(fileDialog.exec_()):
            selectedFiles = fileDialog.selectedFiles()
            jasonFile = selectedFiles[0]
        if(jasonFile is not None):
            #call cadnano json parsing funcality here and pass jasonFile. Check to see if result is correct
            messageBox = QMessageBox()
            messageBox.setText('imported successfully')
            messageBox.exec_()
        else:
            messageBox = QMessageBox()
            messageBox.setText('import nonsuccessful')
            messageBox.show()

    def connect(self,ui_loader):
        ui_loader.mainWindow.import_button_item.clicked.connect(ui_loader.menuItemController.import_button_item_clicked_Slot)


