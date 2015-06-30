__author__ = 'jie'
import sys

from initialization import initAppWithGui


def main(args):
    app = initAppWithGui(args)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
