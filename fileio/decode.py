__author__ = 'jie'
from cadnano.document import Document
from cadnano.fileio import nnodecode
import io
from cadnano.gui.controllers.documentcontroller import DocumentController

import json
class Decoder:
    def __init__(self,toolBarController, path):
        with io.open(path, 'r', encoding='utf-8') as fd:
            dict = json.load(fd)
            self.mainWindow = toolBarController.mainWindow
            self.document = self.nnodecode(dict)

    def nnodecode(self,dict):
        doc = Document()
        doc.mainWindow = self.mainWindow
        doc.dc = DocumentController(doc)
        document = nnodecode.decode(doc,dict)
        return document

