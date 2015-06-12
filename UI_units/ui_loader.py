__author__ = 'jie'

from ui_window import MainWindow
from controller.Menu_items_controller import MenuController


class UiLoader:

    def __init__(self):
        self.mainWindow = MainWindow()
        self.instantiateControllers()
        self.connectActions()

    def connectActions(self):
        self.menuItemController.connect(self)

    def instantiateControllers(self):
        self.menuItemController = MenuController()
