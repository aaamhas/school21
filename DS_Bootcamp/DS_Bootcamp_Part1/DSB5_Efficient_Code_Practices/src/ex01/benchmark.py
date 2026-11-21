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

def map_method(data):
    result = map(lambda i: i if i.split('@')[1].split('.')[0] == 'gmail' else None, data)
    return list(result)

def main():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com']

    loop_time = timeit.timeit(lambda: loop(emails), number=9000)
    comp_time = timeit.timeit(lambda: comprehension(emails), number=9000)
    map_time = timeit.timeit(lambda: map_method(emails), number=9000)
    print(map_method(emails))
    if map_time <= loop_time and map_time <= comp_time:
        print('it is better to use a map')
        if loop_time <= comp_time:
            print(f'{map_time} vs {loop_time} vs {comp_time}')
            
        else:
            print(f'{map_time} vs {comp_time} vs {loop_time}')
            

    elif comp_time <= loop_time and comp_time <= map_time:
        print('it is better to use a list comprehension')
        if loop_time <= map_time:
            print(f'{comp_time} vs {loop_time} vs {map_time}')
            
            
        else:
            print(f'{comp_time} vs {map_time} vs {loop_time}')

    elif loop_time <= map_time and loop_time <= comp_time:
        print("it is better to use a loop")
        if map_time <= comp_time:    
            print(f'{loop_time} vs {map_time} vs {comp_time}')
        else:
            print(f'{loop_time} vs {comp_time} vs {map_time}')
            
    

if __name__ == '__main__':
    main()