import sys

def search(email):
    with open('employees.tsv', 'r', encoding='utf-8') as f:
        for line in f:
            lst = line.split('\t')
            
            if lst[2].strip() == email:
                return lst[0]


def mail(name):
    print(f'{name}, добро пожаловать в нашу команду! '
    'Мы уверены, что работать вместе с тобой будет очень приятно. '
    'Для нас это важно - мы стремимся, '
    'чтобы в компании работались именно такие люди.')

def process():
    s = sys.argv
    if len(s) != 2:
        return
    name = search(s[1])
    if name == None:
        return
    
    mail(search(s[1]))

if __name__ == '__main__':
    process()
