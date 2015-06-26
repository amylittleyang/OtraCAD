__author__ = 'jie'
from cadnano.document import Document
from fileio import domain_decode
import io
from cadnano.gui.controllers.documentcontroller import DocumentController

import json
class Decoder:
    def __init__(self,toolBarController, path):
        with io.open(path, 'r', encoding='utf-8') as fd:
            dictionary = json.load(fd)
            self.mainWindow = toolBarController.mainWindow
            self.document = self.domainDecode(dictionary)

    def domainDecode(self,dict):
        doc = Document()
        doc.mainWindow = self.mainWindow
        doc.dc = DocumentController(doc)
        document = domain_decode.decode(doc,dict)
        return document

