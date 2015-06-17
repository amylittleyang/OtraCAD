__author__ = 'jie'
from PyQt5.QtWidgets import QMessageBox
class DocumentController:
    def __init__(self,doc):
        self.__doc__= doc
        #self.connect()

    #def connect(self):
        #self.__doc__.documentParsedSignal.connect(self.)

    def TestSlot(self):
        plzwork = QMessageBox()
        plzwork.setText('it worked!')
        plzwork.exec_()

