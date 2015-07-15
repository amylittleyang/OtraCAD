__author__ = 'jie'
from PyQt5.QtWidgets import QGraphicsLineItem
from strandrep.toehold_item_controller import ToeholdItemController
class ToeholdItem(QGraphicsLineItem):
    def __init__(self,toeholdList):
        self._toehold_list = toeholdList
        self._toehold_item_controller = ToeholdItemController()
