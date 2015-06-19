__author__ = 'jie'
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
class RipOffDialog(QDialog):
    def __init__(self):
        super(RipOffDialog, self).__init__()
        uic.loadUi('rip_off_dialog.ui', self)
        self.setupUI()

    def setupUI(self):
        pass
