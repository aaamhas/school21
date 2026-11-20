#!/usr/bin/env python3
import os
import sys
import subprocess
def check():
    if 'VIRTUAL_ENV' in os.environ:
        a = os.environ['VIRTUAL_ENV']
        # if os.path.basename(a) != 'karlondo':
            return False
        else:
            return True
    return False

def main():
    if not check():
        raise EnvironmentError("Wrong or no virtual environment activated")
    else:
        with open("to_install.txt", 'w') as f:
            f.write('beautifulsoup4\npytest')
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'to_install.txt'])

        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'freeze'],
            capture_output = True,
            text = True
        )
        with open("requirements.txt", 'w') as f:
            f.write(result.stdout)
        print(result.stdout)
    os.remove("to_install.txt")

if __name__ == '__main__':
    main()