#!/usr/bin/env python3
import timeit
import random
from collections import Counter

def my_counter(data):
    d = dict()
    for i in data:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    return d

def my_top(data):
    d = my_counter(data)
    sorted_items = sorted(d.items(), key=lambda pair: pair[1], reverse=True)
    return sorted_items[:10]


def main():
    lst = [random.randint(0, 100) for _ in range(1000000)]
    print(f'my function: {timeit.timeit(lambda: my_counter(lst), number=1)}')
    print(f'Counter: {timeit.timeit(lambda: Counter(lst), number=1)}')
    print(f'my top: {timeit.timeit(lambda: my_top(lst), number=1)}')
    print(f"Counter's top: {timeit.timeit(lambda: Counter(lst).most_common(10), number=1)}")
    print(my_counter(lst))
    print(my_top(lst))
    # print(Counter(lst).most_common(10))


if __name__ == '__main__':
    main()