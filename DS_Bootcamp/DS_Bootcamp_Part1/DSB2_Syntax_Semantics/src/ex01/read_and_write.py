def read_and_write():
    with open('ds.csv', 'r', encoding='utf-8') as f, open('ds.tsv', 'w', encoding='utf-8', newline = '') as f2:
        for line in f:
            count = 0
            s = line
            for ind in range(len(line)):
                if line[ind] == '"':
                    count+=1
                if (line[ind] == ',') and (count % 2 == 0):
                    s = s[:ind] + "\t" + s[ind+1:]
            f2.write(s)

if __name__ == '__main__':
    read_and_write()
 