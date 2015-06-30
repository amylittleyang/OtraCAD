__author__ = 'jie'
from Queue import *
if __name__ == '__main__':

    q = Queue(maxsize = 0)
    q.put(1)
    q.put(2)
    print q.get()
    k = q.get()
    print k