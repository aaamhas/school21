#!/usr/bin/env python
import sys
import os
import psutil
def read_csv(data):
    with open(data, 'r') as f:
        return f.readlines()

def main():
    a = sys.argv
    if len(a) != 2:
        raise ValueError("the wrong number of arguments")
    data = a[1]
    lst = read_csv(data)
    for i in lst:
        pass
    
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    cpu_times = process.cpu_times()

    print(f'Peak Memory Usage = {mem_info.peak_wset/(1024**3):.3f} GB')
    print(f'User Mode Time + System Mode Time = {cpu_times.user + cpu_times.system:.2f}s')

if __name__ == '__main__':
    try:
        main()
    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)