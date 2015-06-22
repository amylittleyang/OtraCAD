__author__ = 'jie'


if __name__ == '__main__':
    list = [-1,-1,0,-1]
    for i in range(len(list)):
        list[i] = list[i]+1
    try:
        print(any(list))
    except:
        print 'an error'

