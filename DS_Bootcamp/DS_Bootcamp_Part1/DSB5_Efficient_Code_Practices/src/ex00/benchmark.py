#!/usr/bin/env python3
import timeit

def loop(data):
    ans = []
    for i in data:
        if i.split('@')[1].split('.')[0] == 'gmail':
            ans.append(i)
    return ans

def comprehension(data):
    ans = [i for i in data if i.split('@')[1].split('.')[0] == 'gmail']
    return ans

def main():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com']

    loop_time = timeit.timeit(lambda: loop(emails), number=9000)
    comp_time = timeit.timeit(lambda: comprehension(emails), number=9000)
    print(loop(emails))
    print(comprehension(emails))
    if comp_time <= loop_time:
        print('it is better to use a list comprehension')
        print(f'{comp_time} vs {loop_time}')
    else:
        print("it is better to use a loop")
        print(f'{loop_time} vs {comp_time}')
    

if __name__ == '__main__':
    main()