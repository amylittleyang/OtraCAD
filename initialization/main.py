__author__ = 'jie'
import sys

from initialization import initAppWithGui

def main(args):
    app = initAppWithGui(appArgs=None)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
