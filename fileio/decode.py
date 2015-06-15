__author__ = 'jie'
from cadnano.cadnano2_5.cadnano.document import Document
from cadnano.cadnano2_5.fileio import nnodecode
import io

import json
class Decoder:
    def __init__(self,toolBarController, path):
        with io.open(path, 'r', encoding='utf-8') as fd:
            dict = json.load(fd)
            self.document = self.nnodecode(dict)

    def nnodecode(self,dict):
        document = Document()
        nnodecode.decode(document,dict)
        return document

