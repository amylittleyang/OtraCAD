__author__ = 'jie'

def testYield(list):
    temp = iter(list)
    tempStrand = next(temp)
    while tempStrand:
        if tempStrand < 10:
            yield tempStrand
        tempStrand = next(temp,None)

if __name__ == '__main__':
    a = [1,2,3,2]
    for num in a:
        if num == 1:
            a.remove(1)
    print (a)
