__author__ = 'jie'

from UI_units.ui_window import MainWindow
from UI_units.controller.tool_bar_controller import ToolBarController
from UI_units.controller.pathToolbarController import PathToolbarController

class UiLoader:

    def __init__(self):
        self.mainWindow = MainWindow()
        self.instantiateControllers()
        self.connectActions()

    def connectActions(self):
        self.toolBarController.connect()
        self.path_toolbar_controller.connect()

    def instantiateControllers(self):
        self.toolBarController = ToolBarController(self)
        self.path_toolbar_controller = PathToolbarController(self)
