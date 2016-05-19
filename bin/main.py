__author__ = 'jie'
import sys
import os
#!/usr/bin/env python
# encoding: utf-8
LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) 
PROJECT_DIR = os.path.dirname(LOCAL_DIR)
sys.path.append(PROJECT_DIR)
sys.path.insert(0, '.')

def main(args):
    from bin import initAppWithGui
    # use cadnano initialization function
    app = initAppWithGui(args)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
