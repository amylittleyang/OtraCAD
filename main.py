__author__ = 'jie'
import sys
from PyQt5.QtWidgets import QApplication

from appDecorator import AppDecorator

if __name__ == "__main__":
    app = AppDecorator()   # return decorated app object
    loader = UiLoader()
    loader.mainWindow.show()
    sys.exit(app.exec_())
