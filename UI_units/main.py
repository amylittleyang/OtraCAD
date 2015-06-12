__author__ = 'jie'
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    a = QApplication(sys.argv)
    from ui_loader import UiLoader
    loader = UiLoader()
    loader.mainWindow.show()
    sys.exit(a.exec_())
