__author__ = 'jie'
import sys
from PyQt5.QtWidgets import QApplication

from appDecorator import AppDecorator

def main(args):
    app = AppDecorator(args)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
