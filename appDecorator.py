import sys, os

from code import interact

from cadnano.proxyconfigure import proxyConfigure
proxyConfigure('PyQt')
import cadnano.util as util
decode = None
Document = None
DocumentController = None


from PyQt5.QtCore import QObject, QCoreApplication, pyqtSignal, Qt, QEventLoop, QSize

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp, QApplication, QUndoGroup

__author__ = 'jie'
class AppDecorator(QObject):
    documentWasCreatedSignal = pyqtSignal(object)  # doc
    documentWindowWasCreatedSignal = pyqtSignal(object, object)  # doc, window
    def __init__(self,argv):
        self.qApp = QApplication(argv)
        super(CadnanoQt, self).__init__()