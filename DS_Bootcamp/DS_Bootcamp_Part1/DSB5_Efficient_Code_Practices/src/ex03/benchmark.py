#!/usr/bin/env python3
import timeit
import sys
from functools import reduce

def loop(n):
    ans = 0
    for i in range(1, n+1):
        ans += i*i
    return ans

def reduce_f(n):
    return reduce(lambda acc, x: acc + x*x, range(1, n+1))

def read_args():
    a = sys.argv
    if len(a) != 4:
        raise ValueError("the wrong number of arguments")
    
    return a[1], int(a[2]), int(a[3])

def main():

    d = {'loop': loop, 
        'reduce': reduce_f}

    func, num, x = read_args()

    if func not in d.keys():
        raise ValueError("the wrong function")
    print(d[func](x))
    result = timeit.timeit(lambda: d[func](x), number=num) 
    print(result)


if __name__ == '__main__':
    try:
        main()
    except ValueError as e:
        print(e)