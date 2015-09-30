__author__ = 'jie'
import sys
from bin import initAppWithGui

def main(args):
    # use cadnano initialization function
    app = initAppWithGui(args)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
