__author__ = 'jie'

from initialization.ui_window import MainWindow
from UI_units import ToolBarController

class UiLoader:

    def __init__(self):
        self.mainWindow = MainWindow()
        self.instantiateControllers()
        self.connectActions()

    def connectActions(self):
       self.toolBarController.connect()

    def instantiateControllers(self):
        self.toolBarController = ToolBarController(self)
