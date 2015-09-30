__author__ = 'jie'

from cadnano.cnproxy import tapp


global shared_app
shared_app = tapp

global batch
batch = False
global reopen
reopen = False

def getBatch():
    global batch
    return batch

def setBatch(is_batch):
    global batch
    batch = is_batch

def getReopen():
    global reopen
    return reopen

def setReopen(is_reopen):
    global reopen
    reopen = is_reopen

def app():
    global shared_app
    return shared_app

def initAppWithGui(appArgs=None):
    global shared_app
    from bin.appDecorator import AppDecorator
    # 1. Create the application object
    shared_app = AppDecorator(appArgs)
    # 2. Use the object to finish importing and creating
    # application wide objects
    return shared_app


__all__ = ["document", "enum", "decorators", "fileio", "oligo", "part", "strand", "strand", "strandset", "virtualhelix"]
