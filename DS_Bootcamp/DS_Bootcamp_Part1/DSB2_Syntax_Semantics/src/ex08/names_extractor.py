import sys

def names_extractor(name_file):
    with open(name_file, 'r', encoding='utf-8') as f, open('employees.tsv', 'w', encoding='utf-8', newline = '') as f2:
        f2.write("Name\tSurname\tE-mail\n")
        for line in f:
            if line.strip() == '':
                continue
            data = line.split('@')
            f2.write(f"{data[0].split('.')[0].title()}\t{data[0].split('.')[1].title()}\t{line}")

def process():
    s = sys.argv
    if len(s) != 2:
        return
    name_file = s[1]
    names_extractor(name_file)

if __name__ == '__main__':
    process()
            
