__author__ = 'jie'
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
class MainWindow(QMainWindow):
    #somewhere in constructor:
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui_window.ui', self)

