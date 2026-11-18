import sys
class Research:
    def __init__(self, file):
        self.file = file

    def file_reader(self, has_header = True):
        lst  = list()
        count = 0
        with open(self.file) as f:
            for line in f:
                t = line.strip().split(',')
                if count == 0 and has_header:
                    if len(t)!=2:
                        raise ValueError("ошибка")
                else:
                    if len(t)!=2:
                        raise ValueError("ошибка")
                    elif (t[0]+t[1] != '10') and (t[0]+t[1] != '01'):
                        raise ValueError("ошибка")
                    lst.append(list(map(int,t)))
                count+=1
            
            if not lst:
                raise ValueError("ошибка")
        return lst
    class Calculations:
        def counts(self, data):
            heads = 0
            tails = 0
            for i in data:
                if i[0] == 1:
                    heads += 1
                else:
                    tails += 1
            return heads, tails
        def fractions(self, heads, tails):
            return int(10000 * heads/(heads+tails))/10000, int(10000*tails/(heads+tails))/10000

def main():
    s = sys.argv
    if len(s) != 2:
        raise ValueError("ошибка") 
    research = Research(s[1])
    calculator =research.Calculations()
    reader = research.file_reader()
    heads, tails = calculator.counts(reader)
    print(reader)
    print(heads, tails)
    print(*calculator.fractions(heads, tails))

    
if __name__ == '__main__':
    try:
        main()
    except ValueError as e:
        print(e)
    except FileNotFoundError:
        print("ошибка")
    except PermissionError:
        print("ошибка")
