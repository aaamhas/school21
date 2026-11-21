#!/usr/bin/env python3
import timeit
import sys

def loop(data):
    ans = []
    for i in data:
        if i.split('@')[1].split('.')[0] == 'gmail':
            ans.append(i)
    return ans

def comprehension(data):
    ans = [i for i in data if i.split('@')[1].split('.')[0] == 'gmail']
    return ans

def map_method(data):

    result = map(lambda i: i if i.split('@')[1].split('.')[0] == 'gmail' else None, data)
    return list(result)

def filter_method(data):
    result = filter(lambda i: i.split('@')[1].split('.')[0] == 'gmail', data)
    return list(result)

def read_args():
    a = sys.argv
    if len(a) != 3:
        raise ValueError("the wrong number of arguments")
    
    return a[1], a[2]

def main():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
        'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
        'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
        'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
        'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
        'anna@live.com', 'philipp@gmail.com']
    d = {'loop': loop, 
        'list_comprehension': comprehension, 
        'map': map_method, 
        'filter': filter_method}

    func, num = read_args()
    
    if func not in d.keys():
        raise ValueError("the wrong function")

    # print(d[func](emails))
    
    result = timeit.timeit(lambda: d[func](emails), number=int(num)) 
    print(result)

if __name__ == '__main__':
    try:
        main()
    except ValueError as e:
        print(e)