__author__ = 'jie'
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    from ui_loader import UiLoader
    loader = UiLoader()
    loader.mainWindow.show()
    sys.exit(app.exec_())
