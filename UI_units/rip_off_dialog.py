__author__ = 'jie'
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QListWidgetItem
class RipOffDialog(QDialog):
    def __init__(self):
        super(RipOffDialog, self).__init__()
        uic.loadUi('rip_off_dialog.ui', self)
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle('New Rip-off Transformation')
        listW = self.listWidget
        item1 = QListWidgetItem('Select Strand')
        listW.addItem(item1)
        listW.show()


