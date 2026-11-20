#!/usr/bin/env python3
import os

def get_virtual_env():
    if 'VIRTUAL_ENV' in os.environ:
        return os.environ['VIRTUAL_ENV']
    return None

def main():
    virtual_e = get_virtual_env()
    if virtual_e:
        print(f'Your current virtual env is {virtual_e}')
    else:
        print('Virtual env is not activated')

if __name__ == '__main__':
    main()