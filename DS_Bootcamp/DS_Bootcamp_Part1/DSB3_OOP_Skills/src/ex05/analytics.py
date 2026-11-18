from random import randint
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
        def __init__(self, data):
            self.data = data
        def counts(self):
            heads = 0
            tails = 0
            for i in self.data:
                if i[0] == 1:
                    heads += 1
                else:
                    tails += 1
            return heads, tails
        def fractions(self, heads, tails):
            return int(10000 * heads/(heads+tails))/10000, int(10000*tails/(heads+tails))/10000
    
    class Analytics(Calculations):
        def predict_random(self, n):
            lst = []
            for i in range(n):
                num = randint(0,1)
                lst.append([num, 1-num])
            return lst
        
        def predict_last(self):
            return self.data[-1]

        def save_file(self, data, file_name, extension):
            with open(file_name+'.'+extension, 'w', encoding = 'utf-8') as f:
                f.write(str(data))

                