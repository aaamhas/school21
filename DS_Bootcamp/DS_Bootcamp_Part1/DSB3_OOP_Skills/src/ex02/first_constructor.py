import sys
class Research:
    def __init__(self, file):
        self.file = file

    def file_reader(self):
        s = ''
        count = 0
        with open(self.file) as f:
            for line in f:
                t = line.strip().split(',')
                if count == 0:
                    if len(t)!=2:
                        raise ValueError("ошибка")
                else:
                    if len(t)!=2:
                        raise ValueError("ошибка")
                    elif (t[0]+t[1] != '10') and (t[0]+t[1] != '01'):
                        raise ValueError("ошибка")
                s += line
                count+=1
            
            if count < 2:
                raise ValueError("ошибка")
        return s

def main():
    s = sys.argv
    if len(s) != 2:
        raise ValueError("ошибка") 
    research = Research(s[1])
    print(research.file_reader(), end = '')
    
if __name__ == '__main__':
    try:
        main()
    except ValueError as e:
        print(e)
    except FileNotFoundError:
        print("ошибка")
    except PermissionError:
        print("ошибка")
