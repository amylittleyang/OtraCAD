from cadnano.fileio import nnodecode

__author__ = 'jie'
import io
from cadnano.document import Document
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

