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
        super(AppDecorator, self).__init__()
        from cadnano.gui.views.preferences import Preferences
        self.prefs = Preferences()
        #icon = QIcon(ICON_PATH)
        #self.qApp.setWindowIcon(icon)


        self.document_controllers = set()  # Open documents
        self.active_document = None
        self.vh = {}  # Newly created VirtualHelix register here by idnum.
        self.vhi = {}
        self.partItem = None

        global decode
        global Document
        global DocumentController
        from cadnano.document import Document
        from cadnano.fileio.nnodecode import decode
        from cadnano.gui.controllers.documentcontroller import DocumentController
        from cadnano.gui.views.pathview import pathstyles as styles
        # doc = Document()
        # self.d = self.newDocument(base_doc=doc)
        styles.setFontMetrics()

    # def newDocument(self, base_doc=None):
    #     global DocumentController
    #     dc = DocumentController(base_doc)
    #     dc.newDocument()  # tell it to make a new doucment
    #     return dc._document


    def prefsClicked(self):
        self.prefs.showDialog()

    def exec_(self):
        if hasattr(self, 'qApp'):
            from initialization.ui_loader import UiLoader
            loader = UiLoader()
            loader.mainWindow.show()
            self.mainEventLoop = QEventLoop()
            self.mainEventLoop.exec_()
            #self.qApp.exec_()
